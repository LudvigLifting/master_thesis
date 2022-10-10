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
        }
      ]
    }
  }
  render(){
    return (
      <div>
        <Container>
          <Row>
            <div className="jumbotron text-left">
              <h1>Fire extinguisher monitoring app</h1>
              <p>Here you can monitor your things</p>
            </div>
          </Row>
          <Row md="auto">
            <div>
              {this.state.data.map((item) => {
                return( 
                  <Col key={item.id}>
                    <div>
                      <Extinguisher  
                      id={item.id} 
                      batteryLevel={item.batteryLevel} 
                      locationCode={item.locationCode}/>
                    </div>
                  </Col>
                )}
              )}
            </div>
          </Row>
        </Container>
      </div>
    );
  }
}

export default App;
