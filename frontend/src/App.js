import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navigation from './components/Navigation';
import BookList from './components/BookList';
import BookForm from './components/BookForm';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <Navigation />
      <Routes>
        <Route path="/" element={<div className="home"><h1>Добро пожаловать в MyBooks!</h1></div>} />
        <Route path="/books" element={<BookList />} />
        <Route path="/books/create" element={<BookForm onSuccess={() => window.location.href = '/books'} />} />
        <Route path="/authors" element={<div><h1>Авторы (в разработке)</h1></div>} />
        <Route path="/genres" element={<div><h1>Жанры (в разработке)</h1></div>} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;