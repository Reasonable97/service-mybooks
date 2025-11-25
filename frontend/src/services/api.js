import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// ========== Книги ==========

export const getBooks = (page = 1, size = 10) => {
  return api.get('/books', { params: { page, size } });
};

export const getBook = (id) => {
  return api.get(`/books/${id}`);
};

export const createBook = (bookData) => {
  return api.post('/books', bookData);
};

export const updateBook = (id, bookData) => {
  return api.patch(`/books/${id}`, bookData);
};

export const deleteBook = (id) => {
  return api.delete(`/books/${id}`);
};

// ========== Авторы ==========

export const getAuthors = (page = 1, size = 10) => {
  return api.get('/authors', { params: { page, size } });
};

export const getAuthor = (id) => {
  return api.get(`/authors/${id}`);
};

export const createAuthor = (authorData) => {
  return api.post('/authors', authorData);
};

export const updateAuthor = (id, authorData) => {
  return api.patch(`/authors/${id}`, authorData);
};

export const deleteAuthor = (id) => {
  return api.delete(`/authors/${id}`);
};

// ========== Жанры ==========

export const getGenres = (page = 1, size = 10) => {
  return api.get('/genres', { params: { page, size } });
};

export const getGenre = (id) => {
  return api.get(`/genres/${id}`);
};

export const createGenre = (genreData) => {
  return api.post('/genres', genreData);
};

export const updateGenre = (id, genreData) => {
  return api.patch(`/genres/${id}`, genreData);
};

export const deleteGenre = (id) => {
  return api.delete(`/genres/${id}`);
};

export default api;