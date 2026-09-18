import unittest

import torch

from loss import Loss


class OneNormTests(unittest.TestCase):
    def test_matches_direct_formula_and_gradients(self):
        torch.manual_seed(7)
        dims, curvatures = [3, 3], [-0.25, -2.]
        embedding = torch.randn(5, 6, dtype=torch.float64, requires_grad=True)
        raw_theta = torch.randn(2, 3, 2, 3, dtype=torch.float64, requires_grad=True)
        theta = torch.nn.functional.normalize(raw_theta, dim=-1).flatten(-2)
        rho = torch.rand(2, 3, 2, dtype=torch.float64, requires_grad=True)
        logits = torch.randn(2, 3, 5, dtype=torch.float64, requires_grad=True)
        targets = torch.tensor([[0, 2, 4], [3, 1, 0]])
        actual = Loss.bridge_loss_variational_one_norm_refactor(
            logits, targets, rho, theta, embedding, dims, curvatures,
        )
        phis = torch.nn.functional.normalize(embedding.reshape(5, 2, 3), dim=-1)
        k2 = torch.tensor(curvatures, dtype=torch.float64).abs()
        u = rho * k2.sqrt()
        inner = (theta.reshape(2, 3, 2, 3)[:, :, None] * phis[None, None]).sum(-1)
        denom = (u[:, :, None].cosh() - u[:, :, None].sinh() * inner).min(dim=2).values
        # The 1-norm itself, not its 2 (1 - p_y) closed form.
        one_norm = (torch.nn.functional.one_hot(targets, 5) - logits.softmax(-1)).abs().sum(-1)
        expected = one_norm.square() / 2 * (4 * k2 / denom.square()).sum(-1)
        torch.testing.assert_close(actual, expected, rtol=1e-12, atol=1e-12)
        inputs = (logits, rho, raw_theta, embedding)
        for a, b in zip(torch.autograd.grad(actual.sum(), inputs, retain_graph=True),
                        torch.autograd.grad(expected.sum(), inputs)):
            torch.testing.assert_close(a, b, rtol=1e-11, atol=1e-11)

    def test_between_the_angular_surrogate_and_the_variational_ce(self):
        """||P_theta (x - xhat)||^2 <= ||delta_y - p||_1^2 < 2 CE: still an upper
        bound on the shared-D_x angular rate, and strictly below the CE bound."""
        torch.manual_seed(5)
        dims, curvatures = [4, 4], [-1.5, -0.5]
        embedding = torch.randn(7, 8, dtype=torch.float64)
        theta = torch.nn.functional.normalize(
            torch.randn(3, 2, 2, 4, dtype=torch.float64), dim=-1)
        rho = torch.rand(3, 2, 2, dtype=torch.float64) * 3
        logits = torch.randn(3, 2, 7, dtype=torch.float64) * 3
        targets = torch.randint(0, 7, (3, 2))
        args = (logits, targets, rho, theta.flatten(-2), embedding, dims, curvatures)
        one_norm = Loss.bridge_loss_variational_one_norm_refactor(*args)
        vce = Loss.bridge_loss_variational_crossentropy_refactor(*args)
        # The shared-D_x angular rate itself, with the TARGET's D_x.
        phis = torch.nn.functional.normalize(embedding.reshape(7, 2, 4), dim=-1)
        xs = phis[targets]
        err = xs - (logits.softmax(-1)[..., None, None] * phis).sum(-3)
        err = err - (err * theta).sum(-1, keepdim=True) * theta
        k2 = torch.tensor(curvatures, dtype=torch.float64).abs()
        u = rho * k2.sqrt()
        denom = u.cosh() - u.sinh() * (xs * theta).sum(-1)
        surrogate = (9 * k2 / (2 * denom.square()) * err.square().sum(-1)).sum(-1)
        self.assertTrue((surrogate <= one_norm + 1e-12).all())
        self.assertTrue((one_norm < vce).all())

    def test_logit_tails(self):
        """Unit weight (rho = 0, d = 2), so the loss is 2 sigmoid(-gap)^2: exact
        where 1 - softmax_y rounds to 0 (gap 300) and where it saturates (-1000)."""
        embedding = torch.tensor([[1., 0.], [-1., 0.]], dtype=torch.float64)
        for gap in (300., 0.5, -1000.):
            with self.subTest(gap=gap):
                logits = torch.tensor([[[gap, 0.]]], dtype=torch.float64, requires_grad=True)
                actual = Loss.bridge_loss_variational_one_norm_refactor(
                    logits, torch.zeros(1, 1, dtype=torch.long),
                    torch.zeros(1, 1, 1, dtype=torch.float64),
                    embedding[:1].reshape(1, 1, 2), embedding,
                )
                x = torch.tensor(gap, dtype=torch.float64)
                expected = 2 * torch.sigmoid(-x).square()
                torch.testing.assert_close(actual.squeeze(), expected, rtol=1e-13, atol=0)
                gradient, = torch.autograd.grad(actual.sum(), logits)
                g = 2 * expected * torch.sigmoid(x)
                torch.testing.assert_close(
                    gradient.flatten(), torch.stack([-g, g]), rtol=1e-13, atol=0,
                )

    def test_overflowing_weight(self):
        """The weight 255^2 e^{700} overflows float64 on its own; the loss
        2 (1 - p_y)^2 * weight = 2 * 255^2 e^{-100} does not."""
        dim = 256
        embedding = torch.zeros(2, dim, dtype=torch.float64)
        embedding[:, 0] = torch.tensor([1., -1.])
        logits = torch.tensor([[[400., 0.]]], dtype=torch.float64, requires_grad=True)
        result = Loss.bridge_loss_variational_one_norm_refactor(
            logits, torch.zeros(1, 1, dtype=torch.long),
            torch.full((1, 1, 1), 350., dtype=torch.float64),
            embedding[:1].reshape(1, 1, dim), embedding,
        )
        expected = 2 * (dim - 1) ** 2 * torch.exp(torch.tensor(-100., dtype=torch.float64))
        torch.testing.assert_close(result.squeeze(), expected, rtol=1e-12, atol=0)
        gradient, = torch.autograd.grad(result.sum(), logits)
        torch.testing.assert_close(
            gradient.flatten(), torch.stack([-2 * expected, 2 * expected]), rtol=1e-12, atol=0,
        )


if __name__ == '__main__':
    unittest.main()
