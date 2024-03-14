import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [data, setData] = useState(null);
  const [todos, setTodos] = useState([]);
  const [input, setInput] = useState('');

  useEffect(() => {
    fetch('http://localhost:8000/api/test')
      .then(response => response.json())
      .then(data => setData(data));
  }, []);

  const handleAddTodo = () => {
    setTodos([...todos, input]);
    setInput('');
  };

  const handleDeleteTodo = (index) => {
    const newTodos = [...todos];
    newTodos.splice(index, 1);
    setTodos(newTodos);
  };

  return (
    <div className="App">
      <header className="App-header">
        {data ? (
          <div>
            <h1>Data received from API:</h1>
            <pre>{JSON.stringify(data, null, 2)}</pre>
          </div>
        ) : (
          <p>Loading...</p>
        )}

        <div style={{ marginTop: '2rem' }}>
          <h2>Todo List</h2>
          <input
            value={input}
            onChange={e => setInput(e.target.value)}
            style={{ marginRight: '1rem' }}
          />
          <button onClick={handleAddTodo}>Add Todo</button>
          {todos.map((todo, index) => (
            <div key={index} style={{ marginTop: '1rem' }}>
              {todo}
              <button onClick={() => handleDeleteTodo(index)} style={{ marginLeft: '1rem' }}>Delete</button>
            </div>
          ))}
        </div>
      </header>
    </div>
  );
}

export default App;