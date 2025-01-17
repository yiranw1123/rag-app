import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './routes/App.jsx'
import Chat from './routes/chat.jsx'
import './index.css'
import{
  createBrowserRouter,
  RouterProvider,

} from "react-router-dom";
import ErrorPage from './routes/error-page.jsx';
import { Provider } from 'react-redux';
import store from '../src/store/store.js';

const router = createBrowserRouter([
  {
    path: "/",
    element:<App/>,
    errorElement: <ErrorPage/>
  },
  {
    path: "chat",
    element: <Chat/>
  }
])

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
     <Provider store={store}>
     <RouterProvider router={router} />
     </Provider>
  </React.StrictMode>,
)
