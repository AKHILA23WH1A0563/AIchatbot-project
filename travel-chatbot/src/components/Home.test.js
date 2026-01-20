import { render, screen } from "@testing-library/react";
import Home from "./Home";

test("renders Home page title", () => {
  render(<Home />);
  // Using a regex to find the text even if it has <br /> or icons
  expect(screen.getByText(/Make Your Travel/i)).toBeInTheDocument();
  expect(screen.getByText(/Easy/i)).toBeInTheDocument();
});

test("renders chat input field", () => {
  render(<Home />);
  expect(
    screen.getByPlaceholderText(/Ask your travel question/i)
  ).toBeInTheDocument();
});

test("renders navbar buttons", () => {
  render(<Home />);
  // Use fuzzy matching for buttons that now contain icons
  expect(screen.getByText(/New Chat/i)).toBeInTheDocument();
  expect(screen.getByText(/Chat History/i)).toBeInTheDocument();
  expect(screen.getByText(/Light Theme/i)).toBeInTheDocument();
});

test("renders the send button icon", () => {
  render(<Home />);
  expect(screen.getByText("➤")).toBeInTheDocument();
});