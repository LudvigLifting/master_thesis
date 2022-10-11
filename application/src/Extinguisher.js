import React, { Component } from 'react'
import { Card, ListGroupItem } from 'react-bootstrap'
import { ProgressBar } from 'react-bootstrap';
import { ListGroup } from 'react-bootstrap';
//import { ArrowRight } from 'react-bootstrap'

export default class Extinguisher extends Component {
  render() {
    return (
      <Card 
        style={{width: '16rem'}}
        bg={'light'}>
        <Card.Header> id: {this.props.id} </Card.Header>
        <Card.Body>
          <Card.Title> Extinguisher title: {this.props.name} </Card.Title>
          <ListGroup variant="flush">
            <ListGroup.Item>
              <Card.Text>
              This is representing a fire-extinguisher.
              </Card.Text>
            </ListGroup.Item>
            <ListGroup.Item>
              Location code: <h5 >{this.props.locationCode}</h5>
            </ListGroup.Item>
            <ListGroup.Item>
              Pressure:
            </ListGroup.Item>
            <ListGroup.Item>
              <div>
                Battery status:
                <ProgressBar animated variant="success" now={this.props.batteryLevel} label={`${this.props.batteryLevel}%`}></ProgressBar>
              </div>
            </ListGroup.Item>
          </ListGroup>
        </Card.Body>
        <Card.Footer> 
            Last updated: {}
        </Card.Footer>
      </Card>
    )
  }
}

