import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/Navigation.css';

const Navigation = () => {
  return (
    <nav className="navigation">
      <div className="nav-container">
        <Link to="/" className="nav-logo">
          📚 MyBooks
        </Link>
        <ul className="nav-menu">
          <li>
            <Link to="/books" className="nav-link">
              Книги
            </Link>
          </li>
          <li>
            <Link to="/authors" className="nav-link">
              Авторы
            </Link>
          </li>
          <li>
            <Link to="/genres" className="nav-link">
              Жанры
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navigation;