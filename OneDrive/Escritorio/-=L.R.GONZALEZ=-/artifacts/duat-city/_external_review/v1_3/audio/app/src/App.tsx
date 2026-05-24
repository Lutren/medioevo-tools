import { Routes, Route } from 'react-router'
import Home from './pages/Home'
import AudioEnginePage from './pages/AudioEnginePage'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/audio-engine" element={<AudioEnginePage />} />
    </Routes>
  )
}
