
import './App.css'
import { ThemeProvider } from './components/ui/theme-provider'
import HomePage from './pages/HomePage'

function App() {
  return (
    <div >
      <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
        <HomePage />
      </ThemeProvider>
       
      
    </div>
  )
}

export default App
