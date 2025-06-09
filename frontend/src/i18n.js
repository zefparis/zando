import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import fr from './locales/fr.json';
import ln from './locales/ln.json';

i18n
  .use(initReactI18next)
  .init({
    resources: {
      fr: { translation: fr },
      ln: { translation: ln },
    },
    lng: 'fr', // langue par défaut
    fallbackLng: 'fr',
    interpolation: {
      escapeValue: false,
    },
  });

export default i18n;