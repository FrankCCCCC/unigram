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
        xs = torch.nn.functional.normalize(embedding[targets].reshape(2, 3, 2, 3), dim=-1)
        k2 = torch.tensor(curvatures, dtype=torch.float64).abs()
        u = rho * k2.sqrt()
        denom = u.cosh() - u.sinh() * (xs * theta.reshape(2, 3, 2, 3)).sum(-1)
        expected = torch.nn.functional.cross_entropy(
            logits.transpose(1, 2), targets, reduction='none',
        ) * (4 * k2 / denom.square()).sum(-1)
        torch.testing.assert_close(actual, expected, rtol=1e-12, atol=1e-12)
        inputs = (logits, rho, raw_theta, embedding)
        for a, b in zip(torch.autograd.grad(actual.sum(), inputs, retain_graph=True),
                        torch.autograd.grad(expected.sum(), inputs)):
            torch.testing.assert_close(a, b, rtol=1e-11, atol=1e-11)

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
