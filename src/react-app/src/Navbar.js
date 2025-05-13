import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Navbar, Container, Nav, Modal, Button } from "react-bootstrap";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faRightFromBracket, faCircleQuestion } from '@fortawesome/free-solid-svg-icons';
import { FaGithub } from "react-icons/fa";

function NavBar() {
  const navigate = useNavigate();
  const [expanded, setExpanded] = useState(false);
  const [isMobile, setIsMobile] = useState(window.innerWidth < 992);
  const [showHelp, setShowHelp] = useState(false);

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
    <>
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
            className="ms-5 text-white"
            style={{ padding: 0 }}
          >
            <FaGithub />
          </Nav.Link>

          {/* Center: Brand */}
          <div className="text-center">
            <Navbar.Brand as={Link} to="/" onClick={() => setExpanded(false)}>
              <h1 className="display-4 text-warning m-0">Acro<span className="text-white m-0">DB</span></h1>
              <small className="text-white d-block" style={{ fontSize: "1rem" }}>
                Chat-queried NoSQL database for gymnasts and parkour practitioners.
              </small>
            </Navbar.Brand>
          </div>

          {/* Right: Logout + Help + Toggler */}
          <div className="d-flex align-items-center">
            <Nav className="">
              <Nav.Link
                as="button"
                className="me-2 btn btn-link nav-link p-0 text-white"
                onClick={() => setShowHelp(true)}
                title="Help"
              >
                <FontAwesomeIcon icon={faCircleQuestion} />
              </Nav.Link>
              {!isMobile && (
                <Nav.Link
                  as="button"
                  className="btn btn-link nav-link p-0 text-white"
                  onClick={handleLogout}
                  title="Logout"
                >
                  <FontAwesomeIcon icon={faRightFromBracket} />
                </Nav.Link>
              )}
            </Nav>
            <Navbar.Toggle
              onClick={() => setExpanded(!expanded)}
              aria-controls="navbar-content"
              className="border-0"
            />
          </div>

          {/* Collapsed Logout (mobile only) */}
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

      {/* Help Modal */}
      <Modal
        show={showHelp}
        onHide={() => setShowHelp(false)}
        centered
        contentClassName="bg-black text-white border border-white border-opacity-50 rounded"
      >
        <Modal.Header closeButton closeVariant="white">
          <Modal.Title>Need Help?</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <ul className="text-start">
            <li>🔐 Login securely with AWS Cognito (it's free)</li>
            <li>🔑 Input your OpenAI API key to query (your API key is stored in-session and is never sent to our servers) <br/> ... visit <a href="https://platform.openai.com/api-keys" target="_blank">OpenAI's API key page</a></li>
            <li>📝 Ask about skills, moves, or keywords like “MAG Floor” or “show backflips” <br/> ... or if you know the specific ID, even better! Also specify the discipline and event like "MAG Floor ID 1"</li>
            <li>📦 Data is fetched securely from DynamoDB and S3</li>
            <li>📱 Horizontal orientation is recommended for mobile devices</li>
            <li>🧑‍💻 See GitHub (top left icon) or email turangan@usc.edu for direct inquiries</li>
          </ul>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="outline-light" onClick={() => setShowHelp(false)}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}

export default NavBar;
