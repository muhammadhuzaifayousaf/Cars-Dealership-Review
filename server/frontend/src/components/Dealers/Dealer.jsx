import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import "./Dealers.css";
import "../assets/style.css";
import positive_icon from "../assets/positive.png";
import neutral_icon from "../assets/neutral.png";
import negative_icon from "../assets/negative.png";
import review_icon from "../assets/reviewbutton.png";
import Header from '../Header/Header';

const Dealer = () => {
  const [dealer, setDealer] = useState({});
  const [reviews, setReviews] = useState([]);
  const [reviewsLoaded, setReviewsLoaded] = useState(false);
  const params = useParams();
  const id = params.id;

  useEffect(() => {
    const getDealer = async () => {
      try {
        const res = await fetch(`/djangoapp/dealer/${id}`);
        const data = await res.json();
        if (res.ok && data.status === 200 && data.dealer.length > 0) {
          setDealer(data.dealer[0]);
        }
      } catch (error) {
        console.error("Failed to load dealer:", error);
      }
    };

    const getReviews = async () => {
      try {
        const res = await fetch(`/djangoapp/reviews/dealer/${id}`);
        const data = await res.json();
        if (res.ok && data.status === 200) {
          setReviews(data.reviews || []);
        }
      } catch (error) {
        console.error("Failed to load reviews:", error);
      } finally {
        setReviewsLoaded(true);
      }
    };

    getDealer();
    getReviews();
  }, [id]);

  const sentimentIcon = (sentiment) => {
    if (sentiment === "positive") return positive_icon;
    if (sentiment === "negative") return negative_icon;
    return neutral_icon;
  };

  return (
    <div style={{ margin: "20px" }}>
      <Header />
      <div style={{ marginTop: "10px" }}>
        <h1 style={{ color: "grey" }}>
          {dealer.full_name || "Dealership"}
          {sessionStorage.getItem("username") && (
            <Link to={`/postreview/${id}`}>
              <img
                src={review_icon}
                style={{ width: "10%", marginLeft: "10px", marginTop: "10px" }}
                alt="Post Review"
              />
            </Link>
          )}
        </h1>
        <h4 style={{ color: "grey" }}>
          {dealer.city || ""}, {dealer.address || ""}, Zip - {dealer.zip || ""}, {dealer.state || ""}
        </h4>
      </div>

      <div className="reviews_panel">
        {!reviewsLoaded ? (
          <p>Loading Reviews...</p>
        ) : reviews.length === 0 ? (
          <div>No reviews yet!</div>
        ) : (
          reviews.map((review) => (
            <div className="review_panel" key={review.id}>
              <img
                src={sentimentIcon(review.sentiment)}
                className="emotion_icon"
                alt={`${review.sentiment || "neutral"} sentiment`}
              />
              <div className="review">{review.review}</div>
              <div className="reviewer">
                {review.name} {review.car_make} {review.car_model} {review.car_year}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default Dealer;
