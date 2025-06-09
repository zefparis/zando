import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { getAds } from './services/api';
import AdCard from './components/AdCard'; // Importer le nouveau composant

// Dans App.jsx, avant la définition du composant App
const ProtectedRoute = ({ children }) => {
  const { token } = useAuth();
  const navigate = useNavigate();

  React.useEffect(() => {
    if (!token) {
      // Redirige vers la page de connexion si l'utilisateur n'est pas authentifié
      navigate('/login');
    }
  }, [token, navigate]);

  return token ? children : null; // Affiche les enfants si le token existe
};

// Pages (composants vides pour l'instant)
const HomePage = () => {
  const { t } = useTranslation();
  const [ads, setAds] = React.useState([]);
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    const fetchAds = async () => {
      try {
        const response = await getAds();
        setAds(response.data);
      } catch (error) {
        console.error("Erreur lors de la récupération des annonces:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchAds();
  }, []);

  if (loading) {
    return <p>Chargement des annonces...</p>;
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">{t('welcome_message')}</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {ads.length > 0 ? (
          ads.map(ad => <AdCard key={ad.id} ad={ad} />)
        ) : (
          <p>Aucune annonce à afficher pour le moment.</p>
        )}
      </div>
    </div>
  );
};
import { createAd } from './services/api';

const PostAdPage = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [title, setTitle] = React.useState('');
  const [description, setDescription] = React.useState('');
  const [price, setPrice] = React.useState('');
  const [image, setImage] = React.useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('title', title);
    formData.append('description', description);
    formData.append('price', price);
    formData.append('image', image);

    try {
      await createAd(formData);
      alert('Annonce créée avec succès !');
      navigate('/');
    } catch (error) {
      console.error("Erreur lors de la création de l'annonce:", error);
      alert("Erreur lors de la création de l'annonce.");
    }
  };

  return (
    <div className="max-w-2xl mx-auto bg-white p-8 rounded-lg shadow-md">
      <h1 className="text-2xl font-bold mb-6 text-center">{t('post_ad')}</h1>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="title" className="block text-gray-700 font-bold mb-2">Titre</label>
          <input type="text" id="title" value={title} onChange={(e) => setTitle(e.target.value)} className="w-full px-3 py-2 border rounded-lg" required />
        </div>
        <div className="mb-4">
          <label htmlFor="description" className="block text-gray-700 font-bold mb-2">Description</label>
          <textarea id="description" value={description} onChange={(e) => setDescription(e.target.value)} className="w-full px-3 py-2 border rounded-lg" rows="4"></textarea>
        </div>
        <div className="mb-4">
          <label htmlFor="price" className="block text-gray-700 font-bold mb-2">Prix (USD)</label>
          <input type="number" id="price" value={price} onChange={(e) => setPrice(e.target.value)} className="w-full px-3 py-2 border rounded-lg" required />
        </div>
        <div className="mb-6">
          <label htmlFor="image" className="block text-gray-700 font-bold mb-2">Image</label>
          <input type="file" id="image" onChange={(e) => setImage(e.target.files[0])} className="w-full" required />
        </div>
        <button type="submit" className="w-full bg-yellow-400 text-white font-bold py-2 px-4 rounded-lg hover:bg-yellow-500">
          {t('post_ad')}
        </button>
      </form>
    </div>
  );
};
const LoginPage = () => {
  const { t } = useTranslation();
  const { login } = useAuth();
  const navigate = useNavigate();
  const [phone, setPhone] = React.useState('+243');
  const [pin, setPin] = React.useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const success = await login(phone, pin);
    if (success) {
      navigate('/'); // Redirige vers l'accueil après connexion
    } else {
      alert('Échec de la connexion');
    }
  };

  return (
    <div className="max-w-md mx-auto bg-white p-8 rounded-lg shadow-md">
      <h1 className="text-2xl font-bold mb-6 text-center">{t('login')}</h1>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="phone" className="block text-gray-700 font-bold mb-2">Numéro de téléphone</label>
          <input type="tel" id="phone" value={phone} onChange={(e) => setPhone(e.target.value)} className="w-full px-3 py-2 border rounded-lg" required />
        </div>
        <div className="mb-6">
          <label htmlFor="pin" className="block text-gray-700 font-bold mb-2">Code PIN (6 chiffres)</label>
          <input type="password" id="pin" value={pin} onChange={(e) => setPin(e.target.value)} className="w-full px-3 py-2 border rounded-lg" maxLength="6" required />
        </div>
        <button type="submit" className="w-full bg-blue-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-blue-700">
          {t('login')}
        </button>
      </form>
    </div>
  );
};

function App() {
  const { i18n, t } = useTranslation();

  const changeLanguage = (lng) => {
    i18n.changeLanguage(lng);
  };

  return (
    <AuthProvider>
      <Router>
        <div className="bg-gray-100 min-h-screen font-sans">
          <nav className="bg-white shadow-md p-4 flex justify-between items-center">
            <Link to="/" className="text-2xl font-bold text-blue-600">Zando</Link>
            <div>
              <Link to="/post" className="bg-yellow-400 text-white font-bold py-2 px-4 rounded hover:bg-yellow-500 mr-4">
                {t('post_ad')}
              </Link>
              <button onClick={() => changeLanguage('fr')} className="mr-2 font-semibold">🇫🇷 FR</button>
              <button onClick={() => changeLanguage('ln')} className="font-semibold">🇨🇩 LN</button>
            </div>
          </nav>
          <main className="p-8">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/post" element={<ProtectedRoute><PostAdPage /></ProtectedRoute>} />
              <Route path="/login" element={<LoginPage />} />
            </Routes>
          </main>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;