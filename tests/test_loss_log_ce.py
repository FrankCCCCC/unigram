import unittest

import torch

from loss import Loss


class LogCrossEntropyTests(unittest.TestCase):
    def test_sharp_posterior_value_and_gradient(self):
        for dtype in (torch.float32, torch.float64):
            for dim in (2, 3):
                with self.subTest(dtype=dtype, dim=dim):
                    embedding = torch.zeros(2, dim, dtype=torch.float64)
                    embedding[:, 0] = torch.tensor([1., -1.])
                    logits = torch.tensor([[[40., 0.]]], dtype=dtype, requires_grad=True)
                    result = Loss.bridge_loss_variational_crossentropy_refactor(
                        logits, torch.zeros(1, 1, dtype=torch.long),
                        torch.full((1, 1, 1), 20., dtype=torch.float64),
                        embedding[:1].reshape(1, 1, dim), embedding,
                    )
                    expected = float((dim - 1) ** 2)
                    torch.testing.assert_close(result, torch.full_like(result, expected))
                    gradient, = torch.autograd.grad(result.sum(), logits)
                    torch.testing.assert_close(
                        gradient, logits.new_tensor([[[-expected, expected]]]),
                    )

    def test_overflowing_weight_and_underflowing_ce(self):
        dim = 256
        embedding = torch.zeros(2, dim, dtype=torch.float64)
        embedding[:, 0] = torch.tensor([1., -1.])
        logits = torch.tensor([[[800., 0.]]], dtype=torch.float64, requires_grad=True)
        result = Loss.bridge_loss_variational_crossentropy_refactor(
            logits, torch.zeros(1, 1, dtype=torch.long),
            torch.full((1, 1, 1), 350., dtype=torch.float64),
            embedding[:1].reshape(1, 1, dim), embedding,
        )
        expected = (dim - 1) ** 2 * torch.exp(torch.tensor(-100., dtype=torch.float64))
        torch.testing.assert_close(result.squeeze(), expected, rtol=1e-12, atol=0)
        gradient, = torch.autograd.grad(result.sum(), logits)
        torch.testing.assert_close(
            gradient.flatten(), torch.stack([-expected, expected]), rtol=1e-12, atol=0,
        )

    def test_matches_direct_formula_and_gradients(self):
        torch.manual_seed(7)
        dims, curvatures = [3, 3], [-0.25, -2.]
        embedding = torch.randn(5, 6, dtype=torch.float64, requires_grad=True)
        raw_theta = torch.randn(2, 3, 2, 3, dtype=torch.float64, requires_grad=True)
        theta = torch.nn.functional.normalize(raw_theta, dim=-1).flatten(-2)
        rho = torch.rand(2, 3, 2, dtype=torch.float64, requires_grad=True)
        logits = torch.randn(2, 3, 5, dtype=torch.float64, requires_grad=True)
        targets = torch.tensor([[0, 2, 4], [3, 1, 0]])
        actual = Loss.bridge_loss_variational_crossentropy_refactor(
            logits, targets, rho, theta, embedding, dims, curvatures,
        )
        # D_{e_v,m} for EVERY word, then the per-factor minimum: the weight is
        # a function of z_t alone, which is what keeps the Bayes posterior the
        # minimiser (experiments/init_test_log_vce_3d_refactor_new/vce_bayes.md).
        phis = torch.nn.functional.normalize(embedding.reshape(5, 2, 3), dim=-1)
        k2 = torch.tensor(curvatures, dtype=torch.float64).abs()
        u = rho * k2.sqrt()
        inner = (theta.reshape(2, 3, 2, 3)[:, :, None] * phis[None, None]).sum(-1)
        denom = (u[:, :, None].cosh() - u[:, :, None].sinh() * inner).min(dim=2).values
        expected = torch.nn.functional.cross_entropy(
            logits.transpose(1, 2), targets, reduction='none',
        ) * (4 * k2 / denom.square()).sum(-1)
        torch.testing.assert_close(actual, expected, rtol=1e-12, atol=1e-12)
        inputs = (logits, rho, raw_theta, embedding)
        for a, b in zip(torch.autograd.grad(actual.sum(), inputs, retain_graph=True),
                        torch.autograd.grad(expected.sum(), inputs)):
            torch.testing.assert_close(a, b, rtol=1e-11, atol=1e-11)

    def test_weight_only_grows_so_the_bound_survives(self):
        """min_v D_{e_v,m} <= D_{x_m}, so the loss dominates the target-indexed
        form it replaced -- Step B of the derivation stays an upper bound."""
        torch.manual_seed(5)
        dims, curvatures = [4], [-1.5]
        embedding = torch.randn(7, 4, dtype=torch.float64)
        theta = torch.nn.functional.normalize(
            torch.randn(3, 2, 4, dtype=torch.float64), dim=-1)
        rho = torch.rand(3, 2, 1, dtype=torch.float64) * 3
        logits = torch.randn(3, 2, 7, dtype=torch.float64)
        targets = torch.randint(0, 7, (3, 2))
        actual = Loss.bridge_loss_variational_crossentropy_refactor(
            logits, targets, rho, theta, embedding, dims, curvatures)
        # the superseded target-indexed weight, computed directly
        xs = torch.nn.functional.normalize(embedding[targets], dim=-1)
        k2 = torch.tensor(curvatures, dtype=torch.float64).abs()
        u = rho * k2.sqrt()
        denom = u.cosh() - u.sinh() * (xs * theta).sum(-1, keepdim=True)
        ce = torch.nn.functional.cross_entropy(
            logits.reshape(-1, 7), targets.reshape(-1), reduction="none").reshape(3, 2)
        superseded = ce * ((dims[0] - 1) ** 2 * k2 / denom.square()).sum(-1)
        self.assertTrue((actual >= superseded - 1e-12).all())

    def test_weight_does_not_depend_on_the_target(self):
        """The property the whole fix exists for: same z_t, different y, same
        weight -- so the weighted CE stays proper for the Bayes posterior."""
        torch.manual_seed(9)
        dims, curvatures = [3], [-1.0]
        embedding = torch.randn(6, 3, dtype=torch.float64)
        theta = torch.nn.functional.normalize(
            torch.randn(4, 1, 3, dtype=torch.float64), dim=-1)
        rho = torch.rand(4, 1, 1, dtype=torch.float64) * 2
        # Uniform logits make CE identical for every target, so any difference
        # in the result would be the weight and nothing else.
        logits = torch.zeros(4, 1, 6, dtype=torch.float64)
        losses = [
            Loss.bridge_loss_variational_crossentropy_refactor(
                logits, torch.full((4, 1), y), rho, theta, embedding,
                dims, curvatures)
            for y in range(6)
        ]
        for other in losses[1:]:
            torch.testing.assert_close(losses[0], other)

    def test_negative_tail_and_large_wrong_logit(self):
        for gap in (34.999, 35., 35.001, -1000.):
            with self.subTest(gap=gap):
                logits = torch.tensor([[[gap, 0.]]], dtype=torch.float64, requires_grad=True)
                embedding = torch.tensor([[1., 0.], [-1., 0.]], dtype=torch.float64)
                actual = Loss.bridge_loss_variational_crossentropy_refactor(
                    logits, torch.zeros(1, 1, dtype=torch.long),
                    torch.zeros(1, 1, 1, dtype=torch.float64),
                    embedding[:1].reshape(1, 1, 2), embedding,
                )
                x = torch.tensor(-gap, dtype=torch.float64)
                expected = torch.logaddexp(torch.zeros_like(x), x)
                torch.testing.assert_close(actual.squeeze(), expected, rtol=1e-13, atol=0)
                gradient, = torch.autograd.grad(actual.sum(), logits)
                p = torch.sigmoid(x)
                torch.testing.assert_close(gradient.flatten(), torch.stack([-p, p]), rtol=1e-13, atol=0)


if __name__ == '__main__':
    unittest.main()
