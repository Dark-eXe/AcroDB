import React from "react";
import { Link } from "react-router-dom";
import { Navbar, Container } from "react-bootstrap";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faKey } from '@fortawesome/free-solid-svg-icons';

function NavBar() {
  return (
    <Navbar fixed="top" className="px-3 bg-black bg-opacity-75">
      <Container fluid className="d-flex justify-content-between align-items-center">
        <div className="nav-item">
          <Link className="nav-link" to="/auth">
          	<FontAwesomeIcon icon={faKey} />
          </Link>
        </div>

        <Navbar.Brand href="/" className="d-flex align-items-center">
        <Link className="navbar-brand text-warning" to="/">
					<h1 className="display-4 text-warning">Acro<span className="display-4 text-white">DB</span></h1>
					<small className="text-white">Chat-queried NoSQL database for gymnasts and parkour practitioners.</small>
        </Link>
        </Navbar.Brand>

        <div className="d-flex gap-3">
          <a
            href="https://github.com/Dark-eXe/AcroDB"
            target="_blank"
            rel="noopener noreferrer"
            className="btn btn-outline-light btn-sm"
          >
            GitHub
          </a>
        </div>
      </Container>
    </Navbar>
  );
}

export default NavBar;
