import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Navbar, Container, Nav, Modal, Button } from "react-bootstrap";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faRightFromBracket, faCircleQuestion } from '@fortawesome/free-solid-svg-icons';
import { AiFillOpenAI } from "react-icons/ai";
import { FaAws } from "react-icons/fa";

function NavBar() {
  const navigate = useNavigate();
  const [showHelp, setShowHelp] = useState(false);


  const handleLogout = () => {
    sessionStorage.removeItem("openai_api_key");
    sessionStorage.removeItem("aws_creds");
    sessionStorage.removeItem("cognito_id_token");
    navigate("/auth");
  };

  return (
    <>
      <Navbar
        bg="black"
        variant="dark"
        fixed="top"
        className="bg-opacity-75 px-3"
      >
        <Container fluid>
          {/* Left: GitHub */}
          <Nav.Link
            as="button"
            className="me-2 btn btn-link nav-link p-0 text-white"
            onClick={() => setShowHelp(true)}
            title="Help"
          >
            <div className=" btn btn-outline-light">
              <FontAwesomeIcon icon={faCircleQuestion} />
            </div>
          </Nav.Link>
          {/* Center: Brand */}
          <div className="text-center m-0">
            <Navbar.Brand as={Link} to="/">
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
                className="btn btn-link nav-link p-0 text-white"
                onClick={handleLogout}
                title="Logout"
              >
                <div className=" btn btn-outline-light">
                  <FontAwesomeIcon icon={faRightFromBracket} />
                </div>
              </Nav.Link>
            </Nav>
          </div>
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
            <li><button className="btn btn-outline-warning btn-sm mb-2"><FaAws/></button> Login securely with AWS (it's free)</li>
            <li><button className="btn btn-outline-warning btn-sm"><AiFillOpenAI/></button> Input your OpenAI API key to query <br/> 
              {/*eslint-disable-next-line*/}
              <em><small>- your API key is session-scoped and never sent to our servers, visit <a href="https://platform.openai.com/api-keys" target="_blank">OpenAI's API key page</a> </small></em> <br/>
              <em><small>*non-OpenAI and cost-free LLM planned for future</small></em>
            </li>
            <hr/>
            <li>📝 Ask about skills, moves, or keywords like “MAG Floor” or “show backflips” <br/> ... or if you know the specific ID, even better! Also specify the discipline and event</li>
            <li><small>ex. "WAG Vault ID 1"</small></li>
            <hr/>
            <li>📦 Data fetched securely from DynamoDB and S3</li>
            <li>📱 Horizontal orientation recommended for mobile devices</li>
            {/*eslint-disable-next-line*/}
            <li>🧑‍💻 See <a href="https://github.com/Dark-eXe/AcroDB" target="_blank"><small>GitHub</small></a> or email <small>turangan@usc.edu</small> for direct inquiries</li>
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
