import React, { Component } from "react";
import { Grid, Typography } from "@material-ui/core";


export default class InactiveError extends Component {
    constructor(props) {
        super(props);
    }
    
    render() {
        return <Grid container direction="row" alignItems="center">
        <Grid item xs={12}>
          <Typography align="center">Test</Typography>
        </Grid>
      </Grid>
    }
}