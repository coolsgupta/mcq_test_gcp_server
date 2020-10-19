import React, {Component} from "react";
import {Link, useHistory} from "react-router-dom";
import Constant from "./Constant"
import Container from "@material-ui/core/Container";
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import {makeStyles, createStyles, Theme} from '@material-ui/core/styles';

export default class MainPage extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            userEmail: '',
            categories: [],
            catQuestionBank: {},
            userScoreReports: []
        };
    }

    get_question_set() {

        fetch(Constant.Server_Url+'get_categories')
            .then(response => response.json())
            .then(data => {
                this.setState({categories: data.data})

            });
    }

    componentDidMount() {
        let email = sessionStorage.getItem("userEmail")
        if (email == null) {
            this.props.history.push('/')
        }
        this.get_question_set()
        this.get_all_score_reports(email)


    }

    categorySelected(value) {
        console.log(value)
        Constant.categorySelected = value;
        console.log(this.props)
        this.props.history.push(`/test`)

    }

    get_all_score_reports(uEmail) {
        console.log(uEmail)
        this.setState({userEmail: uEmail})

        fetch(Constant.Server_Url+'get_user_score_reports?email=' + uEmail)
            .then(response => response.json())
            .then(data => {
                console.log(data)
                if (data.success) {
                    this.setState({userScoreReports: data.data});

                }
            })
            .catch(error => console.error(error))

    }

    render() {
        const classes = makeStyles((theme: Theme) =>
            createStyles({
                root: {
                    flexGrow: 1,
                },
                paper: {
                    height: 140,
                    width: 100,
                    backgroundColor: '#aaa'
                },
                control: {
                    padding: theme.spacing(2),
                },
            }),
        );
        return (
            <Container style={{backgroundColor: '#fff', marginTop: "50px"}} component="main" maxWidth="xl">


                <Grid container className={classes.root} spacing={10}>

                    <Grid item xs={12}>
                        <h3> Select your category</h3>
                        <Grid container justify="center" spacing={10}>
                            {this.state.categories.map((o, k) => (
                                <Grid key={k} item>
                                    <Paper className={classes.paper}>
                                        <div class="table-primary" style={{
                                            display: 'flex',
                                            height: '100px',
                                            width: '200px',
                                            justifyContent: 'center',
                                            alignItems: "center",
                                            textAlign: "center",
                                            fontColor:"#fff"

                                        }} onClick={() => {
                                            this.categorySelected(o)
                                        }}>
                                            <span style={{fontColor:"#fff"}}>{o}</span>
                                        </div>
                                    </Paper>
                                </Grid>
                            ))}
                        </Grid>
                        <hr />
                        <Grid item xs={12} style={{marginTop:'20px'}}>
                            <h4>Your previous Score Reports</h4>

                            <Grid container justify="center" spacing={100}>
                                <table class="table table-striped"  >
                                    <tr class="table-primary">
                                        <th>No.</th>
                                        <th>Date</th>
                                        <th>Category</th>
                                        <th>Max Points</th>
                                        <th>Correct</th>
                                        <th>Incorrect</th>
                                        <th>Unattempted</th>
                                    </tr>
                                    {this.state.userScoreReports.map((o, k) => {
                                        return (
                                            <tr key={k}>
                                                <td>{k + 1}</td>
                                                <td>{o.Date}</td>
                                                <td>{o.category_selected}</td>
                                                <td>{o.total_questions}</td>
                                                <td style={{fontColor:"green"}}>{o.score}</td>
                                                <td>{o.wrong}</td>
                                                <td>{o.unattempted}</td>

                                            </tr>


                                        )
                                    })
                                    }
                                </table>

                            </Grid>
                        </Grid>
                    </Grid>
                </Grid>


            </Container>
        );
    }
}
