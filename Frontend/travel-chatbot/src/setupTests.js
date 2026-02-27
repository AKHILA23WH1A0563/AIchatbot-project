import "@testing-library/jest-dom";
const originalError = console.error;
beforeAll(() => {
  console.error = (...args) => {
    if (
      args[0]?.includes("ReactDOMTestUtils.act") ||
      args[0]?.includes("React Router Future Flag")
    ) {
      return;
    }
    originalError(...args);
  };
});
