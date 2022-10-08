import mongoose from "mongoose";

const connectDB = async () => {
    if (mongoose.connections[0].readyState) { // If DB is already connected
        console.log("Already connected to the DB");
        return;
    }

    mongoose.connect(process.env.MONGODB_URI, {}, (err) => {
        if (err) throw err;
        console.log("Connected to mongodb");
    });
};

export default connectDB;