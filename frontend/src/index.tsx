import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import './index.css';

// Mount React app
const rootElement = document.getElementById('root');
if (rootElement) {
  ReactDOM.render(<App />, rootElement);
} else {
  // Fallback: create root element if it doesn't exist
  const newRoot = document.createElement('div');
  newRoot.id = 'root';
  document.body.appendChild(newRoot);
  ReactDOM.render(<App />, newRoot);
}
