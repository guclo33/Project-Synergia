import React from 'react';
import './App.css';
import { RouterProvider, createBrowserRouter, createRoutesFromElements, Route } from 'react-router-dom';
import {Home} from "./pages/home/Home"
import {Register} from "./pages/register/Register"
import {Login} from "./pages/login/Login"
import {Admin} from "./pages/admin/Admin"
import {Leader} from "./pages/leader/Leader"
import {User} from "./pages/user/User"


const appRouter = createBrowserRouter(createRoutesFromElements(
  <>
    <Route path="/" element={<Home />} />
    <Route path="/register" element={<Register />}/>
    <Route path="/login" element={<Login />} />
    <Route path="/admin" element={<Admin />} />
    <Route path="/leader" element={<Leader />} />
    <Route path="/user" element={<User />} />  
  </>

))
;


function App() {
  return (
    <RouterProvider router={appRouter} />
  );
}

export default App;
