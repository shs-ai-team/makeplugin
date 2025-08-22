import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoadingPage from './components/LoadingPage';
import PluginGeneratorPage from './components/PluginGeneratorPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoadingPage />} />
        <Route path="/plugin-generator" element={<PluginGeneratorPage />} />
      </Routes>
    </Router>
  );
}

export default App;
