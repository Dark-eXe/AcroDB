import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Navbar, Container, Nav } from "react-bootstrap";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faRightFromBracket } from '@fortawesome/free-solid-svg-icons';
import { FaGithub } from "react-icons/fa";

function NavBar() {
  const navigate = useNavigate();
  const [expanded, setExpanded] = useState(false);
  const [isMobile, setIsMobile] = useState(window.innerWidth < 992);

  // Track screen size for mobile toggle detection
  useEffect(() => {
    const handleResize = () => setIsMobile(window.innerWidth < 992);
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  const handleLogout = () => {
    sessionStorage.removeItem("openai_api_key");
    sessionStorage.removeItem("aws_creds");
    sessionStorage.removeItem("cognito_id_token");
    setExpanded(false);
    navigate("/auth");
  };

  return (
    <Navbar
      bg="black"
      variant="dark"
      expand="lg"
      expanded={expanded}
      fixed="top"
      className="bg-opacity-75 px-3"
    >
      <Container fluid>
        {/* Left: GitHub */}
        <Nav.Link
          href="https://github.com/Dark-eXe/AcroDB"
          target="_blank"
          rel="noopener noreferrer"
          className="text-white"
          style={{ padding: 0 }}
        >
          <FaGithub />
        </Nav.Link>

        {/* Center: Brand */}
        <div className="flex-grow-1 text-center">
          <Navbar.Brand as={Link} to="/" onClick={() => setExpanded(false)}>
            <h1 className="display-3 text-warning m-0">Acro<span className="text-white">DB</span></h1>
            <small className="text-white d-block" style={{ fontSize: "1rem" }}>
              Chat-queried NoSQL database for gymnasts and parkour practitioners.
            </small>
          </Navbar.Brand>
        </div>

        {/* Right: Logout (desktop) + Toggler */}
        <div className="d-flex align-items-center">
          {!isMobile && (
            <Nav className="me-2">
              <Nav.Link
                as="button"
                className="btn btn-link nav-link p-0 text-white"
                onClick={handleLogout}
                title="Logout"
              >
                <FontAwesomeIcon icon={faRightFromBracket} />
              </Nav.Link>
            </Nav>
          )}
          <Navbar.Toggle
            onClick={() => setExpanded(!expanded)}
            aria-controls="navbar-content"
            className="border-0"
          />
        </div>

        {/* Collapsed Logout (mobile only, when expanded) */}
        {isMobile && expanded && (
          <Navbar.Collapse id="navbar-content" className="d-lg-none mt-2">
            <Nav className="flex-column align-items-end">
              <Nav.Link
                as="button"
                className="btn btn-link nav-link p-0 text-white"
                onClick={handleLogout}
              >
                <FontAwesomeIcon icon={faRightFromBracket} /> Logout
              </Nav.Link>
            </Nav>
          </Navbar.Collapse>
        )}
      </Container>
    </Navbar>
  );
}

export default NavBar;
