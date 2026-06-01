import { h, render } from 'https://esm.sh/preact@10.19.6';
import htm from 'https://esm.sh/htm@3.1.1';
import App from './App.js';

const html = htm.bind(h);

// Mount the App component
render(html`<${App} />`, document.getElementById('root'));
console.log("Voiceflow Clone Initialized successfully.");
