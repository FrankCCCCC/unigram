import unittest

import torch

from loss import Loss


class BrierTests(unittest.TestCase):
    def test_matches_direct_formula_and_gradients(self):
        torch.manual_seed(7)
        dims, curvatures = [3, 3], [-0.25, -2.]
        embedding = torch.randn(5, 6, dtype=torch.float64, requires_grad=True)
        raw_theta = torch.randn(2, 3, 2, 3, dtype=torch.float64, requires_grad=True)
        theta = torch.nn.functional.normalize(raw_theta, dim=-1).flatten(-2)
        rho = torch.rand(2, 3, 2, dtype=torch.float64, requires_grad=True)
        logits = torch.randn(2, 3, 5, dtype=torch.float64, requires_grad=True)
        targets = torch.tensor([[0, 2, 4], [3, 1, 0]])
        actual = Loss.bridge_loss_variational_brier_refactor(
            logits, targets, rho, theta, embedding, dims, curvatures,
        )
        phis = torch.nn.functional.normalize(embedding.reshape(5, 2, 3), dim=-1)
        k2 = torch.tensor(curvatures, dtype=torch.float64).abs()
        u = rho * k2.sqrt()
        inner = (theta.reshape(2, 3, 2, 3)[:, :, None] * phis[None, None]).sum(-1)
        denom = (u[:, :, None].cosh() - u[:, :, None].sinh() * inner).min(dim=2).values
        brier = (torch.nn.functional.one_hot(targets, 5) - logits.softmax(-1)).square().sum(-1)
        # c/2 = 2 (V - 1) / V = 1.6 at V = 5.
        expected = 1.6 * brier * (4 * k2 / denom.square()).sum(-1)
        torch.testing.assert_close(actual, expected, rtol=1e-12, atol=1e-12)
        inputs = (logits, rho, raw_theta, embedding)
        for a, b in zip(torch.autograd.grad(actual.sum(), inputs, retain_graph=True),
                        torch.autograd.grad(expected.sum(), inputs)):
            torch.testing.assert_close(a, b, rtol=1e-11, atol=1e-11)

    def test_between_one_norm_and_its_worst_case(self):
        """brier / one_norm = (V-1)/V (1 + ||r||^2): 1 when the wrong mass is
        spread evenly, 2 (V-1)/V when one word holds it, in between otherwise --
        so the 1-norm's upper bound survives, loosened by at most 2 (V-1)/V."""
        torch.manual_seed(5)
        V = 7
        embedding = torch.randn(V, 4, dtype=torch.float64)
        theta = torch.nn.functional.normalize(torch.randn(3, 1, 4, dtype=torch.float64), dim=-1)
        rho = torch.rand(3, 1, 1, dtype=torch.float64) * 3
        targets = torch.zeros(3, 1, dtype=torch.long)
        even = torch.zeros(3, 1, V, dtype=torch.float64)
        even[..., 0] = 2.
        lone = torch.full((3, 1, V), -60., dtype=torch.float64)
        lone[..., 0], lone[..., 1] = 2., 0.

        def ratio(logits):
            args = (logits, targets, rho, theta, embedding)
            return (Loss.bridge_loss_variational_brier_refactor(*args)
                    / Loss.bridge_loss_variational_one_norm_refactor(*args))

        worst = 2 * (V - 1) / V
        torch.testing.assert_close(ratio(even), torch.ones(3, 1, dtype=torch.float64), rtol=1e-12, atol=0)
        torch.testing.assert_close(ratio(lone), torch.full((3, 1), worst, dtype=torch.float64), rtol=1e-12, atol=0)
        noisy = ratio(torch.randn(3, 1, V, dtype=torch.float64) * 3)
        self.assertTrue(((noisy > 1) & (noisy < worst)).all())

    def test_bayes_posterior_is_the_optimum(self):
        """The weight is target-free, so at a fixed z_t the posterior-expected
        loss is c/2 W ||p - q||^2 + const: zero logit gradient at p = q, and any
        other p scores worse."""
        torch.manual_seed(3)
        V, d = 6, 3
        embedding = torch.randn(V, d, dtype=torch.float64)
        theta = torch.nn.functional.normalize(
            torch.randn(d, dtype=torch.float64), dim=0).expand(V, 1, d).contiguous()
        rho = torch.full((V, 1, 1), 0.8, dtype=torch.float64)
        targets = torch.arange(V)[:, None]
        q = torch.distributions.Dirichlet(torch.ones(V, dtype=torch.float64)).sample()

        def expected_loss(logits):
            return (q * Loss.bridge_loss_variational_brier_refactor(
                logits.expand(V, 1, V), targets, rho, theta, embedding)[:, 0]).sum()

        logits = q.log().requires_grad_(True)
        gradient, = torch.autograd.grad(expected_loss(logits), logits)
        torch.testing.assert_close(gradient, torch.zeros_like(gradient), rtol=0, atol=1e-12)
        other = torch.distributions.Dirichlet(torch.ones(V, dtype=torch.float64)).sample()
        self.assertLess(expected_loss(q.log()), expected_loss(other.log()))

    def test_sharp_posterior_under_overflowing_weight(self):
        """The weight 255^2 e^{700} overflows float64 on its own and 1 - p_y =
        2 e^{-400} rounds to 0 through softmax; with the two wrong logits equal,
        ||r||^2 = 1/2 and the loss is 2 (1 - p_y)^2 * weight = 8 * 255^2 e^{-100}."""
        dim = 256
        embedding = torch.zeros(3, dim, dtype=torch.float64)
        embedding[:, 0] = torch.tensor([1., -1., -1.])
        logits = torch.tensor([[[400., 0., 0.]]], dtype=torch.float64, requires_grad=True)
        result = Loss.bridge_loss_variational_brier_refactor(
            logits, torch.zeros(1, 1, dtype=torch.long),
            torch.full((1, 1, 1), 350., dtype=torch.float64),
            embedding[:1].reshape(1, 1, dim), embedding,
        )
        expected = 8 * (dim - 1) ** 2 * torch.exp(torch.tensor(-100., dtype=torch.float64))
        torch.testing.assert_close(result.squeeze(), expected, rtol=1e-12, atol=0)
        gradient, = torch.autograd.grad(result.sum(), logits)
        torch.testing.assert_close(
            gradient.flatten(), torch.stack([-2 * expected, expected, expected]), rtol=1e-12, atol=0,
        )


if __name__ == '__main__':
    unittest.main()
