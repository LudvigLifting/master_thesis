import React, { useState, Component } from "react";
import Extinguisher from "./Extinguisher";
import 'bootstrap/dist/css/bootstrap.min.css';
import { Container, Row, Col } from "react-bootstrap";
import { v4 as uuid } from 'uuid';

class App extends Component {
  constructor(props){
    super(props);
    this.state = {
      data : [
        {
          "batteryLevel" : 10,
          "locationCode" : 1111
        },
        {
          "batteryLevel" : 50,
          "locationCode" : 2222
        },
        {
          "batteryLevel" : 100,
          "locationCode" : 3333
        },
        {
          "batteryLevel" : 75,
          "locationCode" : 4444
        },
        {
          "batteryLevel" : 75,
          "locationCode" : 5555
        },
        {
          "batteryLevel" : 75,
          "locationCode" : 6666
        },
        {
          "batteryLevel" : 75,
          "locationCode" : 7777
        }
      ]
    }
  }
  render(){
    return (
        <Container>
          <Row>
            <div className="jumbotron text-left">
              <h1>Fire extinguisher monitoring app</h1>
              <p>Here you can monitor your things</p>
            </div>
          </Row>
          <Row fluid>
              {this.state.data.map((item, index) => {
                return(
                  <Col key={index}>
                    <p>
                      <Extinguisher
                      id={uuid()}
                      batteryLevel={item.batteryLevel}
                      locationCode={item.locationCode}/>
                    </p>
                  </Col>
                )}
              )}
          </Row>
        </Container>
    );
  }
}

export default App;
