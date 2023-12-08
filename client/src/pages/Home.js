import React, { useState, useEffect } from "react";
import {
  Container,
  Row,
  Col,
  Card,
  Button,
  Form,
  Modal,
} from "react-bootstrap";
import "./home.css";

import axios from "axios";

const Home = () => {
  const [selectedCity, setSelectedCity] = useState("Islamabad");
  const [selectedPropertyType, setSelectedPropertyType] = useState("Apartment");
  const [houseSize, setHouseSize] = useState("");
  const [numberOfBedrooms, setNumberOfBedrooms] = useState("");
  const [dataColumns, setDataColumns] = useState([]);
  const [selectedLocation, setSelectedLocation] = useState("");
  const [predictedPrice, setPredictedPrice] = useState(null); // State to store predicted price
  const [showModal, setShowModal] = useState(false);
  // const [showModal2, setShowModal2] = useState(false);
  const [predictedPriceAnn, setPredictedPriceAnn] = useState(null);

  useEffect(() => {
    // Dynamically import JSON data based on the selected city
    const fetchData = async () => {
      const cityData = await import(
        `../data/${selectedCity.toLowerCase()}.json`
      );
      setDataColumns(cityData.data_columns);
    };

    fetchData();
  }, [selectedCity]);

  const handleCityChange = (event) => {
    setSelectedCity(event.target.value);
    // Update selected location based on the selected city
    setSelectedLocation("");
  };

  const handlePropertyTypeChange = (event) => {
    setSelectedPropertyType(event.target.value);
  };

  const handleHouseSizeChange = (event) => {
    setHouseSize(event.target.value);
  };

  const handleNumberOfBedroomsChange = (event) => {
    setNumberOfBedrooms(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    // Divide houseSize by 20 and store in formData
    const adjustedHouseSize = houseSize / 20;

    const formData = {
      city: selectedCity,
      propertyType: selectedPropertyType,
      houseSize: adjustedHouseSize,
      numberOfBedrooms,
      location: selectedLocation,
    };

    console.log("Form data:", formData);
    try {
      // Make a POST request to the Flask server
      const response = await axios.post(
        "http://localhost:4000/toPredictPrice",
        formData
      );

      // Update the predicted prices in the state
      setPredictedPrice(response.data.predicted_price_linear_reg);
        setPredictedPriceAnn(response.data.predicted_price_ann);
        console.log("Response:", response);

      // Show the modal
      setShowModal(true);
    } catch (error) {
      console.log("Full error response:", error.response);
    }
    console.log("Predicted price:", predictedPrice);
    console.log("Predicted price:", predictedPriceAnn);
    

  };

  return (
    <Container fluid className="home-container">
      <div className="background-image"></div>
      <Row className="content-container">
        <Col>
          <h3 className="predict-heading">Let's predict your house price</h3>
        </Col>
        <Col>
          <Card className="custom-card">
            <Card.Body>
              <Card.Title>Upload your data</Card.Title>
              <Form onSubmit={handleSubmit}>
                <Form.Group controlId="citySelect">
                  <Form.Label>Select City</Form.Label>
                  <Form.Select value={selectedCity} onChange={handleCityChange}>
                    {[
                      "Islamabad",
                      "Lahore",
                      "Karachi",
                      "Faisalabad",
                      "Rawalpindi",
                    ].map((city) => (
                      <option key={city} value={city}>
                        {city}
                      </option>
                    ))}
                  </Form.Select>
                </Form.Group>

                {/* Populate location options based on the selected city */}
                <Form.Group controlId="locationSelect">
                  <Form.Label>Select Location</Form.Label>
                  <Form.Select
                    value={selectedLocation}
                    onChange={(e) => setSelectedLocation(e.target.value)}
                  >
                    {dataColumns.map((location) => (
                      <option key={location} value={location}>
                        {location}
                      </option>
                    ))}
                  </Form.Select>
                </Form.Group>

                <Form.Group controlId="propertyTypeSelect">
                  <Form.Label>Select Property Type</Form.Label>
                  <Form.Select
                    value={selectedPropertyType}
                    onChange={handlePropertyTypeChange}
                  >
                    {[
                      "Apartment",
                      "House",
                      "Penthouse",
                      "Farm House",
                      "Lower Portion",
                      "Upper Portion",
                    ].map((propertyType) => (
                      <option key={propertyType} value={propertyType}>
                        {propertyType}
                      </option>
                    ))}
                  </Form.Select>
                </Form.Group>

                <Form.Group controlId="houseSizeInput">
                  <Form.Label>House Size (In marlas)</Form.Label>
                  <Form.Control
                    type="number"
                    value={houseSize}
                    onChange={handleHouseSizeChange}
                  />
                </Form.Group>

                <Form.Group controlId="numberOfBedroomsInput">
                  <Form.Label>Number of Bedrooms</Form.Label>
                  <Form.Control
                    type="number"
                    value={numberOfBedrooms}
                    onChange={handleNumberOfBedroomsChange}
                  />
                </Form.Group>

                <Button variant="primary" type="submit">
                  Predict Price
                </Button>
              </Form>
              
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Predicted Prices</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <p>
            Linear Regression Predicted Price: <h3>{predictedPrice}</h3>
          </p>
          <p>
            ANN Predicted Price: <h3>{predictedPriceAnn}</h3>
          </p>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowModal(false)}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>
    </Container>
  );
};

export default Home;
