const express = require('express');
const mongoose = require('mongoose');
const path = require('path');
const fs = require('fs');
const cors = require('cors');

const app = express();
const port = process.env.PORT || 3030;

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: false }));

const reviewsData = JSON.parse(
  fs.readFileSync(path.join(__dirname, 'data', 'reviews.json'), 'utf8')
);
const dealershipsData = JSON.parse(
  fs.readFileSync(path.join(__dirname, 'data', 'dealerships.json'), 'utf8')
);

const Reviews = require('./review');
const Dealerships = require('./dealership');

app.get('/', (req, res) => {
  res.send('Welcome to the Mongoose API');
});

app.get('/fetchReviews', async (req, res) => {
  try {
    res.json(await Reviews.find());
  } catch (error) {
    res.status(500).json({ error: 'Error fetching reviews' });
  }
});

app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    res.json(await Reviews.find({ dealership: req.params.id }));
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealer reviews' });
  }
});

app.get('/fetchDealers', async (req, res) => {
  try {
    res.json(await Dealerships.find());
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealerships' });
  }
});

app.get('/fetchDealers/:state', async (req, res) => {
  try {
    const dealers = await Dealerships.find({
      state: { $regex: `^${req.params.state}$`, $options: 'i' }
    });
    res.json(dealers);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealerships by state' });
  }
});

app.get('/fetchDealer/:id', async (req, res) => {
  try {
    const dealer = await Dealerships.findOne({ id: Number(req.params.id) });
    if (!dealer) {
      return res.status(404).json({ error: 'Dealership not found' });
    }
    res.json(dealer);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealership' });
  }
});

app.post('/insert_review', async (req, res) => {
  try {
    const data = req.body;
    const latest = await Reviews.findOne().sort({ id: -1 });
    const newId = latest ? latest.id + 1 : 1;

    const review = new Reviews({
      id: newId,
      name: data.name,
      dealership: Number(data.dealership),
      review: data.review,
      purchase: data.purchase === true || data.purchase === 'true',
      purchase_date: data.purchase_date,
      car_make: data.car_make,
      car_model: data.car_model,
      car_year: Number(data.car_year)
    });

    res.json(await review.save());
  } catch (error) {
    console.error('Error inserting review:', error.message);
    res.status(500).json({ error: 'Error inserting review' });
  }
});

async function startServer() {
  try {
    await mongoose.connect(
      process.env.MONGODB_URI || 'mongodb://mongo_db:27017/dealershipsDB'
    );

    // Load the sample data only when the collections are empty.
    if (await Dealerships.countDocuments() === 0) {
      await Dealerships.insertMany(dealershipsData.dealerships);
    }
    if (await Reviews.countDocuments() === 0) {
      await Reviews.insertMany(reviewsData.reviews);
    }

    app.listen(port, '0.0.0.0', () => {
      console.log(`Server is running on port ${port}`);
    });
  } catch (error) {
    console.error('Failed to start API:', error.message);
    process.exit(1);
  }
}

startServer();
