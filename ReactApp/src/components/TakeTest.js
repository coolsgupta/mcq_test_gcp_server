import {render} from "@testing-library/react";
import React from "react";
import {Link} from "react-router-dom";
import Constant from "./Constant"
import Container from "@material-ui/core/Container";
import Grid from "@material-ui/core/Grid";
import Paper from "@material-ui/core/Paper";
import Button from "@material-ui/core/Button";

export default class TakeTest extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            question_set: [],
            categories: Constant.categories,
            catQuestionBank: [],
            userAnswerObj: {}
        };
    }

    componentDidMount() {
        let email = sessionStorage.getItem("userEmail")

        if (email == null) {
            this.props.history.push('/')
        }
        this.getQuestions()

    }


    getQuestions() {
        fetch(Constant.Server_Url+'fetch_question_set?category=' + Constant.categorySelected)
            .then(response => response.json())
            .then(data => {
                this.setState({catQuestionBank: data})
                data.map((o) => {
                        this.state.userAnswerObj[o.question_id.toString()] = null
                    }
                )
            })
            .catch(error => console.error(error))
    }

    onSelectAnswer(question, value) {
        console.log("onSelctAs", question, value)
        this.state.userAnswerObj[question.toString()] = value
    }

    onSubmit() {
        console.log(this.state.userAnswerObj)
        let email = sessionStorage.getItem("userEmail")

        let request_body = {
            'attempted_answers': this.state.userAnswerObj,
            'email': email,
            'category_selected': Constant.categorySelected
        }
        const requestOptions = {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(request_body)
        };

        fetch(Constant.Server_Url+'evaluate_response', requestOptions)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    this.props.history.push("/homepage")
                }
                console.log("API Response", data)

            })
            .catch(error => console.error(error))

    }

    render() {
        return (


            <Container style={{backgroundColor: '#fff', paddingTop: "10px"}} component="main" maxWidth="s">
                <div>
                    <h1> Category:{Constant.categorySelected}</h1>
                    {this.state.catQuestionBank.map((o, k) => {
                        return (
                            <div key={k} style={{
                                borderColor: '#333',
                                borderBottomWidth: '10px',
                                marginTop: "10px",
                                marginBottom: "15px",
                                padding: '10px'
                            }}>
                                <span style={{fontColor: '#333', fontSize: '14px'}}>
                                    <span
                                        style={{fontWeight: 'bold', fontSize: "16px"}}>{k + 1})</span> <span>{o.question_text.replaceAll("<br />","\n")}</span>
                                </span>
                                <div style={{
                                    backgroundColor: "#eee",
                                    padding: "5px",
                                    margin: "10px",
                                    borderRadius: '10px'
                                }}>
                                    {
                                        Object.keys(o.answers).map((key, index) => (
                                            <p style={{backgroundColor: '#eee', fontSize: "14px"}} key={index}>
                                                <input onClick={() => {
                                                    this.onSelectAnswer(o.question_id, key)
                                                }} type="radio" id={key} name={o.question_id} value={o.answers[key]}/>
                                                <label htmlFor={key}>{o.answers[key]}</label><br/>
                                            </p>
                                        ))

                                    }
                                </div>
                                <hr/>
                            </div>

                        )
                    })
                    }

                    <div style={{
                        display: 'flex',
                        justifyContent: "center",
                        alignContent: "center",
                        padding: '10px',
                        margin: '10px'
                    }}>
                        <Button
                            type="submit"
                            style={{width: '50%'}}
                            variant="contained"
                            color="secondary"
                            onClick={() => {
                                this.onSubmit()
                            }}
                        >
                            Submit Test
                        </Button>
                    </div>
                </div>

            </Container>


        )
    }


}