import React, { useState, useEffect } from 'react';
import { getBooks, deleteBook } from '../services/api';
import BookForm from './BookForm';
import '../styles/BookList.css';


const BookList = () => {
  const [books, setBooks] = useState([]);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [error, setError] = useState(null);

  const pageSize = 10;


  useEffect(() => {
    fetchBooks();
  }, [page]);


  const fetchBooks = async () => {
    try {
      setLoading(true);
      const response = await getBooks(page, pageSize);
      setBooks(response.data.items);
      setTotal(response.data.total);
    } catch (err) {
      setError('Ошибка при загрузке книг: ' + err.message);
    } finally {
      setLoading(false);
    }
  };


  const handleDelete = async (id) => {
    if (window.confirm('Вы уверены?')) {
      try {
        await deleteBook(id);
        fetchBooks();
      } catch (err) {
        alert('Ошибка при удалении: ' + err.message);
      }
    }
  };


  if (loading) return <div>Загрузка...</div>;
  if (error) return <div className="error">{error}</div>;


  const totalPages = Math.ceil(total / pageSize);


  return (
    <div className="book-list">
      <div className="books-header">
        <h1>Книги</h1>
        <button className="btn btn-primary" onClick={() => setShowForm(true)}>
          + Добавить книгу
        </button>
      </div>

      {showForm && (
        <BookForm
          onSuccess={() => {
            setShowForm(false);
            fetchBooks();
          }}
          onClose={() => setShowForm(false)}
        />
      )}

      <div className="books-grid">
        {books.map((book) => (
          <div key={book.id} className="book-card">
            <h3>{book.title}</h3>
            {book.year && <p>Год: {book.year}</p>}
            {book.authors.length > 0 && (
              <p className="authors">
                Авторы: {book.authors.map((a) => a.name).join(', ')}
              </p>
            )}
            {book.genres.length > 0 && (
              <p className="genres">
                Жанры: {book.genres.map((g) => g.name).join(', ')}
              </p>
            )}
            <div className="book-actions">
              <button onClick={() => handleDelete(book.id)} className="btn-delete">
                Удалить
              </button>
            </div>
          </div>
        ))}
      </div>


      {/* Пагинация */}
      <div className="pagination">
        <button
          onClick={() => setPage(Math.max(1, page - 1))}
          disabled={page === 1}
        >
          Назад
        </button>
        <span>
          Страница {page} из {totalPages} (всего: {total})
        </span>
        <button
          onClick={() => setPage(Math.min(totalPages, page + 1))}
          disabled={page === totalPages}
        >
          Далее
        </button>
      </div>
    </div>
  );
};


export default BookList;
