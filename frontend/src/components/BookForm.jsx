import React, { useState, useEffect } from 'react';
import { createBook, updateBook, getAuthors, getGenres } from '../services/api';
import '../styles/BookForm.css';

const BookForm = ({ bookId, onSuccess }) => {
  const [title, setTitle] = useState('');
  const [year, setYear] = useState('');
  const [authorIds, setAuthorIds] = useState([]);
  const [genreIds, setGenreIds] = useState([]);
  const [authors, setAuthors] = useState([]);
  const [genres, setGenres] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDropdownData();
  }, []);

  const fetchDropdownData = async () => {
    try {
      const authResponse = await getAuthors(1, 100);
      const genreResponse = await getGenres(1, 100);
      setAuthors(authResponse.data.items);
      setGenres(genreResponse.data.items);
    } catch (err) {
      setError('Ошибка при загрузке данных: ' + err.message);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const bookData = {
      title,
      year: year ? parseInt(year) : null,
      author_ids: authorIds,
      genre_ids: genreIds,
    };

    try {
      if (bookId) {
        await updateBook(bookId, bookData);
      } else {
        await createBook(bookData);
      }
      onSuccess();
    } catch (err) {
      setError('Ошибка при сохранении: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="book-form">
      <h2>{bookId ? 'Редактировать книгу' : 'Создать новую книгу'}</h2>

      {error && <div className="error">{error}</div>}

      <div className="form-group">
        <label>Название:</label>
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
      </div>

      <div className="form-group">
        <label>Год:</label>
        <input
          type="number"
          value={year}
          onChange={(e) => setYear(e.target.value)}
          min="1000"
          max="2100"
        />
      </div>

      <div className="form-group">
        <label>Авторы:</label>
        <select
          multiple
          value={authorIds.map(String)}
          onChange={(e) =>
            setAuthorIds(Array.from(e.target.selectedOptions, (opt) => parseInt(opt.value)))
          }
        >
          {authors.map((author) => (
            <option key={author.id} value={author.id}>
              {author.name}
            </option>
          ))}
        </select>
      </div>

      <div className="form-group">
        <label>Жанры:</label>
        <select
          multiple
          value={genreIds.map(String)}
          onChange={(e) =>
            setGenreIds(Array.from(e.target.selectedOptions, (opt) => parseInt(opt.value)))
          }
        >
          {genres.map((genre) => (
            <option key={genre.id} value={genre.id}>
              {genre.name}
            </option>
          ))}
        </select>
      </div>

      <button type="submit" disabled={loading}>
        {loading ? 'Сохранение...' : 'Сохранить'}
      </button>
    </form>
  );
};

export default BookForm;