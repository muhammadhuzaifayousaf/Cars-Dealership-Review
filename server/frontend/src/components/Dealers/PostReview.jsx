import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import "./Dealers.css";
import "../assets/style.css";
import Header from '../Header/Header';

const PostReview = () => {
  const [dealer, setDealer] = useState({});
  const [review, setReview] = useState("");
  const [model, setModel] = useState("");
  const [year, setYear] = useState("");
  const [date, setDate] = useState("");
  const [carmodels, setCarmodels] = useState([]);
  const { id } = useParams();

  const postreview = async () => {
    const name =
      `${sessionStorage.getItem("firstname")} ${sessionStorage.getItem("lastname")}`
        .includes("null")
        ? sessionStorage.getItem("username")
        : `${sessionStorage.getItem("firstname")} ${sessionStorage.getItem("lastname")}`;

    if (!model || !review.trim() || !date || !year) {
      alert("All details are mandatory");
      return;
    }

    const modelSplit = model.split(" ");
    if (modelSplit.length < 2) {
      alert("Please choose a valid car make and model");
      return;
    }

    const jsoninput = JSON.stringify({
      name,
      dealership: id,
      review,
      purchase: true,
      purchase_date: date,
      car_make: modelSplit[0],
      car_model: modelSplit.slice(1).join(" "),
      car_year: year,
    });

    try {
      const res = await fetch("/djangoapp/add_review", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: jsoninput,
      });

      const data = await res.json();

      if (res.ok && data.status === 200) {
        window.location.href = `/dealer/${id}`;
      } else {
        alert(data.message || "Unable to submit review. Please try again.");
      }
    } catch (error) {
      console.error("Failed to submit review:", error);
      alert("Unable to submit review. Please try again.");
    }
  };

  useEffect(() => {
    const getDealer = async () => {
      try {
        const res = await fetch(`/djangoapp/dealer/${id}`);
        const data = await res.json();

        if (res.ok && data.status === 200 && data.dealer?.length > 0) {
          setDealer(data.dealer[0]);
        }
      } catch (error) {
        console.error("Failed to load dealer:", error);
      }
    };

    const getCars = async () => {
      try {
        const res = await fetch("/djangoapp/get_cars");
        const data = await res.json();

        if (res.ok && Array.isArray(data.CarModels)) {
          setCarmodels(data.CarModels);
        } else {
          setCarmodels([]);
        }
      } catch (error) {
        console.error("Failed to load car models:", error);
      }
    };

    getDealer();
    getCars();
  }, [id]);

  return (
    <div>
      <Header />
      <div style={{ margin: "5%" }}>
        <h1 style={{ color: "darkblue" }}>{dealer.full_name}</h1>

        <textarea
          id="review"
          cols="50"
          rows="7"
          value={review}
          onChange={(e) => setReview(e.target.value)}
          placeholder="Write your review"
        />

        <div className="input_field">
          Purchase Date{" "}
          <input
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
          />
        </div>

        <div className="input_field">
          Car Make{" "}
          <select
            name="cars"
            id="cars"
            value={model}
            onChange={(e) => setModel(e.target.value)}
          >
            <option value="" disabled>
              Choose Car Make and Model
            </option>
            {carmodels.map((car, index) => (
              <option
                key={`${car.CarMake}-${car.CarModel}-${index}`}
                value={`${car.CarMake} ${car.CarModel}`}
              >
                {car.CarMake} {car.CarModel}
              </option>
            ))}
          </select>
        </div>

        <div className="input_field">
          Car Year{" "}
          <input
            type="number"
            value={year}
            onChange={(e) => setYear(e.target.value)}
            max={2023}
            min={2015}
          />
        </div>

        <div>
          <button className="postreview" onClick={postreview}>
            Post Review
          </button>
        </div>
      </div>
    </div>
  );
};

export default PostReview;
