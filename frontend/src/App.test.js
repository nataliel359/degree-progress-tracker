import { fireEvent, render, screen } from "@testing-library/react";
import App from "./App";

test("opens password recovery from the sign-in page", () => {
  render(<App />);

  fireEvent.click(screen.getByRole("link", { name: /forgot your password/i }));

  expect(
    screen.getByRole("heading", { name: /forgot your password/i })
  ).toBeInTheDocument();
});

test("renders the reset page for an unprefixed reset link", () => {
  window.history.pushState(
    {},
    "",
    "/reset-password?token=test-reset-token"
  );

  render(<App />);

  expect(
    screen.getByRole("heading", { name: /choose a new password/i })
  ).toBeInTheDocument();
});
