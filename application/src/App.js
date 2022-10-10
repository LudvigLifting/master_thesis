import React, { useState, Component } from "react";
import Extinguisher from "./Extinguisher";
import 'bootstrap/dist/css/bootstrap.min.css';
import { Container, Row, Col } from "react-bootstrap";

class App extends Component {
  constructor(props){
    super(props);
    this.state = {
      data : [
        {
          "id" : 1,
          "batteryLevel" : 10,
          "locationCode" : 1111
        },
        {
          "id" : 2,
          "batteryLevel" : 50,
          "locationCode" : 2222
        },
        {
          "id" : 3,
          "batteryLevel" : 100,
          "locationCode" : 3333
        },
        {
          "id" : 4,
          "batteryLevel" : 75,
          "locationCode" : 4444
        },
        {
          "id" : 5,
          "batteryLevel" : 75,
          "locationCode" : 5555
        },
        {
          "id" : 6,
          "batteryLevel" : 75,
          "locationCode" : 6666
        },
        {
          "id" : 7,
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
              {this.state.data.map((item) => {
                return(
                  <Col key={item.id}>
                    <p>
                      <Extinguisher
                      id={item.id}
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
