import React, { useState } from 'react';
import {
  Collapse,
  Navbar,
  NavbarToggler,
  NavbarBrand,
  Nav,
  NavItem,
  NavLink
} from 'reactstrap';

const Navigation = (props) => {
  const [isOpen, setIsOpen] = useState(false);

  const toggle = () => setIsOpen(!isOpen);

  let navButton =  <NavLink href="/login">Login</NavLink>
  if ( localStorage.getItem('token') ){
    navButton = <NavLink href="/logout">Logout</NavLink>
    }

  return (
    <div>
      <Navbar color="light" light expand="md">
        <NavbarBrand href="/">
          <img
            src="/logo.png"
            width="30"
            height="30"
            className="d-inline-block align-top"
            alt="logo"
          /> ExamNow
        </NavbarBrand>
        <NavbarToggler onClick={toggle} />
        <Collapse isOpen={isOpen} navbar>
          <Nav className="mr-auto" navbar>
            <NavItem>
              <NavLink href="/">Profile</NavLink>
            </NavItem>
            <NavItem>
              <NavLink href="/exam">Exam</NavLink>
            </NavItem>
            <NavItem>
              <NavLink href="/report">Report</NavLink>
            </NavItem>
          </Nav>
          {navButton}
        </Collapse>
      </Navbar>
    </div>
  );
}

export default Navigation;