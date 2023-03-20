import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import MemberList from './MemberList';
import MPVoting from './components/MPVoting';
import styles from './App.module.css';

const App: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  return (
    <div>
      <h1>Hello, React with TypeScript!</h1>
      <div className={styles.filter__wrapper}>
      <input
    type="text"
    placeholder="Search Members"
    value={searchTerm}
    className={styles.search__input}
    onChange={(e) => setSearchTerm(e.target.value)}
  />
  </div>
      <Router>
        <Routes>
          <Route path="/" element={<MemberList searchTerm={searchTerm} />} />
          <Route path="/mp/:memberId/votes/:voteType" element={<MPVoting />} />
        </Routes>
      </Router>
    </div>
  );
};

export default App;
