import React, { Component } from "react";
import { render } from "react-dom";

export default class Participant extends Component {
    constructor(props) {
        super(props);

        this.state = {
            num_participants: 0,
            num_questions: 0,
            is_host: false, 
            // session_id: 0
        };

        this.session_code = this.props.match.params.session_code;
        this.validateSessionActive = this.validateSessionActive.bind(this);

        this.validateSessionActive();
        this.getParticipantSessionInfo();
        // this.props.updateState();
    }

    validateSessionActive = () => {
        fetch('/api/active-session?session_code=' + this.session_code)
            .then((response) => {
                console.log("RESPONSE", response.status);
                if (response.status !== 200)
                    this.props.history.push("/");
            }
        );
    }
        
    getParticipantSessionInfo() {
        console.log("TEST", this.props.match.params);
        fetch('/api/get-session?session_code=' + this.session_code).then((response) => 
            response.json()
        ).then((data) => {
            this.setState({
                num_participants: data.num_participants,
                num_questions: data.num_questions,
                is_host: data.is_host,
                // session_id: data.id
            });
        });
    }


    render() {
        return <div>
                    <p>{this.session_code}</p>
                    <p>{this.state.num_participants}</p>
                    <p>{this.state.num_questions}</p>
                    {/* <p>{this.state.session_id}</p> */}
                    <p>{this.state.is_host.toString()}</p>
               </div>;
    }
}