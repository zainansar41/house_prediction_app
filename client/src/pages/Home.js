import React, { useState, useEffect } from "react";
import { Container, Row, Col, Card, Button, Form } from "react-bootstrap";
import "./home.css";

// ... (existing imports)

const Home = () => {
  const [selectedCity, setSelectedCity] = useState("Islamabad");
  const [selectedPropertyType, setSelectedPropertyType] = useState("Apartment");
  const [houseSize, setHouseSize] = useState("");
  const [numberOfBedrooms, setNumberOfBedrooms] = useState("");
  const [dataColumns, setDataColumns] = useState([]);
  const [selectedLocation, setSelectedLocation] = useState("");

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

  const handleSubmit = (event) => {
    event.preventDefault();

    // Divide houseSize by 20 and store in formData
    const adjustedHouseSize = houseSize / 20;

    const formData = {
      city: selectedCity,
      propertyType: selectedPropertyType,
      houseSize: adjustedHouseSize, // Store the adjusted houseSize
      numberOfBedrooms,
      location: selectedLocation,
    };

    console.log("Form data:", formData);
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
                    {["Apartment", "House", "Plot"].map((propertyType) => (
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
    </Container>
  );
};

export default Home;
