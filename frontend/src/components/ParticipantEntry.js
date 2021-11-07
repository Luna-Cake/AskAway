import React, { Component } from "react";
import { render } from "react-dom";
import { Button, Typography, Textfield, FormHelperText, FormControl, Radio, RadioGroup, FormControlLabel, Grid, TextField } from "@material-ui/core";
import { Link } from "react-router-dom";
// import Alert from '@mui/material/Alert';

export default class ParticipantEntry extends Component {
    constructor(props) {
        super(props);

        this.state = {
            session_code: "",
            error: false,
            error_message: ""
        }
        this.handleCodeEnter = this.handleCodeEnter.bind(this);
        this.handleJoinSession = this.handleJoinSession.bind(this);
    }

    handleCodeEnter(e) {
        this.setState({
            session_code: e.target.value,
        });
    }

    handleJoinSession() {
        const request = {
            method: "POST",
            headers: {"Content-Type": "application/json"}
        }
        console.log("SESSION CODE", this.state.session_code);
        fetch("/api/join-session?session_code=" + this.state.session_code, request).then((response) => {
            // response = response.json();
            // console.log("RESPONSE JSON:", response);
            if (response.status === 200) {
                console.log("SUCCESS");
                this.props.history.push("/session/" + this.state.session_code)
            }

        });
    }

    render() {
        return <Grid container spacing={1}>
                    <Grid item xs={12} align="center">
                        <Typography component="h4" variant="h4">
                            Join an existing room by entering a code!!
                        </Typography>
                    </Grid>
                    <Grid item xs={12} align="center">
                        <FormControl component="fieldset">
                            <TextField size="small" id="outlined-basic" label="Session Code" variant="outlined" onChange={this.handleCodeEnter}/>
                        </FormControl>
                    </Grid>
                    <Grid item xs={12} align="center">
                        <Button variant="contained" color="primary" onClick={this.handleJoinSession}>Join Session</Button>
                    </Grid>
                    <Grid item xs={12} align="center">
                        <Button variant="contained" color="secondary" to="/" component={Link}>Go Back</Button>
                    </Grid>
                </Grid>
    }
}