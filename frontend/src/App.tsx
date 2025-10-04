import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Layout } from '@/components/layout/Layout';
import { Landing } from '@/pages/Landing';
import { GenerationWizard } from '@/pages/GenerationWizard';
import { GameDetails } from '@/pages/GameDetails';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/games/new" element={<GenerationWizard />} />
          <Route path="/games/:id" element={<GameDetails />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
