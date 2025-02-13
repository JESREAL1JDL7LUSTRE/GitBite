import './App.css';
import Item from './pages/Item';

function App() {
  return (
    <div className="bg-yellow-300 h-screen flex justify-center items-center">
      <div className="w-full max-w-3xl p-4">
        <h1 className="text-2xl font-bold text-center mb-4">Customer</h1>
        <Item />
      </div>
    </div>
  );
}

export default App;
