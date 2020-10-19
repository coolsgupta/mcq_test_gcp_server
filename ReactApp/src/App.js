import React, {Component} from 'react';
import logo from './logo.svg';
import './App.css';
import {BrowserRouter, Route, Switch} from 'react-router-dom';
import MainPage from './components/MainPage';
import TakeTest from './components/TakeTest'
import UserLogin from './components/login'

function App() {
    return (
        <main>
            <Switch>
                <Route path='/' component={UserLogin} exact/>
                <Route path='/homepage' component={MainPage}/>
                <Route path='/test' component={TakeTest}/>
            </Switch>
        </main>

    );
}

export default App;
