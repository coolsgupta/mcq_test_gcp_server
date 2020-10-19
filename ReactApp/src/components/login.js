import React, {Component} from "react";
import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import Link from '@material-ui/core/Link';
import Grid from '@material-ui/core/Grid';
import Box from '@material-ui/core/Box';
import Typography from '@material-ui/core/Typography';
import {makeStyles} from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';
import Constant from "./Constant";

function Copyright() {
    return (
        <Typography variant="body2" color="textSecondary" align="center">
            {'Copyright © '}
            <Link color="inherit" href="https://material-ui.com/">
                Sachin Gupta
            </Link>{' '}
            {new Date().getFullYear()}
            {'.'}
        </Typography>
    );
}


export default class UserLogin extends Component {
    useStyles() {
        return (
            makeStyles((theme) => ({
                paper: {
                    marginTop: theme.spacing(10),
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                },
                avatar: {
                    margin: theme.spacing(1),
                    backgroundColor: theme.palette.secondary.main,
                },
                form: {
                    width: '100%', // Fix IE 11 issue.
                    marginTop: theme.spacing(1),
                },
                submit: {
                    margin: theme.spacing(3, 0, 2),
                },
            }))
        )
    };

    constructor(props) {
        super(props);

        this.state = {
            email: null
        };
    }

    componentDidMount() {
        sessionStorage.clear()
    }

    onSubmit() {
        console.log("Iam clicked")
        let request_body = {
            'email': this.state.email
        }
        const requestOptions = {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(request_body)
        };

        fetch(Constant.Server_Url+'register_user', requestOptions)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log(data)
                    sessionStorage.setItem("userEmail", this.state.email)
                    this.props.history.push('/homepage')
                } else {
                    alert("Error in login")
                }


            })
            .catch(error => console.error(error))

    }

    render() {

        const classes = this.useStyles()

        return (
            <Container component="main" maxWidth="xs">
                <CssBaseline/>
                <div style={{marginTop: "100px"}} className={classes.paper}>

                    <Typography component="h1" variant="h5">
                        Enter your email to get started
                    </Typography>
                    <TextField
                        variant="outlined"
                        margin="normal"
                        required
                        fullWidth
                        id="email"
                        label="Email Address"
                        name="email"
                        autoComplete="email"
                        autoFocus
                        onChange={(event) => {
                            this.setState({email: event.target.value})
                        }}
                    />


                    <Button
                        type="submit"
                        fullWidth
                        variant="contained"
                        color="primary"
                        onClick={() => {
                            this.onSubmit()
                        }}
                    >
                        Sign In
                    </Button>

                </div>
                <Box mt={8}>
                    <Copyright/>
                </Box>
            </Container>

        )

    }
}