import React from "react";
import { Link } from "react-router-dom";
import { useNavigate } from 'react-router-dom';
import { Navbar, Container } from "react-bootstrap";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faRightFromBracket} from '@fortawesome/free-solid-svg-icons';
import { FaGithub } from "react-icons/fa";

function NavBar() {
  const navigate = useNavigate();

  const handleLogout = () => {
    sessionStorage.removeItem("openai_api_key");
    sessionStorage.removeItem("aws_creds");
    sessionStorage.removeItem("cognito_id_token");
    navigate("/auth");
  };

  return (
    <Navbar fixed="top" className="px-3 bg-black bg-opacity-75">
      <Container fluid className="d-flex justify-content-between align-items-center">

        <div className="">
          <a
            href="https://github.com/Dark-eXe/AcroDB"
            target="_blank"
            rel="noopener noreferrer"
            className="nav-link"
          >
            <FaGithub />
          </a>
        </div>

        <div className="d-flex align-items-center">
          <Link className="navbar-brand text-warning" to="/">
            <h1 className="display-4 text-warning">Acro<span className="display-4 text-white">DB</span></h1>
            <small className="text-white">Chat-queried NoSQL database for gymnasts and parkour practitioners.</small>
          </Link>
        </div>

        <div className="d-flex">
          <button className="btn btn-link nav-link p-0" onClick={handleLogout} title="Logout">
            <FontAwesomeIcon icon={faRightFromBracket} />
          </button>
        </div>

      </Container>
    </Navbar>
  );
}

export default NavBar;
