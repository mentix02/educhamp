import Navbar from "react-bootstrap/Navbar";
import Container from "react-bootstrap/Container";

export default function Navigation() {
  return (
    <Navbar bg="primary" data-bs-theme="dark">
      <Container>
        <Navbar.Brand className="mb-0 h1">Educhamp Survey</Navbar.Brand>
      </Container>
    </Navbar>
  );
}
