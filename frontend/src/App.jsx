import { Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import Converter from './pages/Converter'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/converter" element={<Converter />} />
    </Routes>
  )
}

export default App
