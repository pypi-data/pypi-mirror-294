import ccxt
import pandas as pd
import numpy as np
import tensorflow as tf
import joblib
import pandas_ta as ta  # For technical indicators like ATR

# Load the model and scaler
model = tf.keras.models.load_model('eth_lstm_best_model.h5')
scaler = joblib.load('scaler.pkl')

# Initialize Binance API
binance = ccxt.binance()

# Function to fetch the current price
def fetch_current_price(symbol):
    try:
        ticker = binance.fetch_ticker(symbol)
        return ticker['last']
    except Exception as e:
        print(f"Error fetching current price: {str(e)}")
        return None

# Function to fetch historical OHLCV data
def fetch_ohlcv(symbol, timeframe='1h', limit=500):
    try:
        ohlcv = binance.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        return df
    except Exception as e:
        print(f"Error fetching OHLCV data: {str(e)}")
        return None

# Function to fetch the latest 48 close prices in real-time (30-minute intervals)
def fetch_latest_data(symbol='ETH/USDT', timeframe='30m', limit=48):
    try:
        ohlcv = binance.fetch_ohlcv(symbol, timeframe, limit=limit)
        return np.array([x[4] for x in ohlcv])  # Return the close prices
    except Exception as e:
        print(f"Error fetching latest data: {str(e)}")
        return None

# Function to calculate ATR
def calculate_atr(ohlcv_df, period=14):
    return ta.atr(ohlcv_df['high'], ohlcv_df['low'], ohlcv_df['close'], length=period).iloc[-1]

# Function to calculate support and resistance levels
def calculate_support_resistance(ohlcv_df):
    support_level = ohlcv_df['low'].min()  # Simplistic approach; for a real strategy, use more advanced methods
    resistance_level = ohlcv_df['high'].max()
    return support_level, resistance_level

# Function to calculate average stop loss
def calculate_average_stop_loss(stop_loss_atr, stop_loss_sr):
    return (stop_loss_atr + stop_loss_sr) / 2

def show_live_price():
    symbol = 'ETH/USDT'
    
    # Fetch current price
    current_price = fetch_current_price(symbol)
    if current_price is not None:
        print(f"\nLive Ethereum Price: ${round(current_price, 2)}")
    else:
        print("Unable to fetch the current price.")

def make_prediction_and_suggest_stop_loss():
    symbol = 'ETH/USDT'
    
    # Fetch current price
    current_price = fetch_current_price(symbol)
    if current_price is None:
        print("Unable to fetch the current price. Exiting.")
        return
    
    # Fetch the latest 48 data points (30-minute intervals)
    latest_data = fetch_latest_data(symbol=symbol, timeframe='30m', limit=48)
    if latest_data is None or len(latest_data) < 48:
        print('Not enough data to make a prediction. Exiting.')
        return
    
    # Preprocess the data
    latest_data = latest_data.reshape(-1, 1)
    latest_data_scaled = scaler.transform(latest_data)
    latest_data_scaled = latest_data_scaled.reshape(1, latest_data_scaled.shape[0], 1)
    
    # Make prediction
    prediction = model.predict(latest_data_scaled)
    predicted_price_1h_ahead = scaler.inverse_transform(prediction).flatten()[0]
    
    # Calculate the percentage change
    percentage_change = ((predicted_price_1h_ahead - current_price) / current_price) * 100
    
    # Fetch historical data
    ohlcv_df = fetch_ohlcv(symbol)
    if ohlcv_df is None:
        print("Unable to fetch OHLCV data. Exiting.")
        return

    # Calculate ATR
    atr = calculate_atr(ohlcv_df)

    # Calculate Support and Resistance levels
    support_level, resistance_level = calculate_support_resistance(ohlcv_df)

    # Calculate stop loss based on ATR
    stop_loss_atr = current_price - (atr * 2) if percentage_change > 0 else current_price + (atr * 2)

    # Calculate stop loss based on Support/Resistance
    stop_loss_sr = support_level if percentage_change > 0 else resistance_level

    # Calculate average stop loss
    average_stop_loss = calculate_average_stop_loss(stop_loss_atr, stop_loss_sr)

    # Determine Buy/Sell suggestion
    if percentage_change > 0.5 and predicted_price_1h_ahead > resistance_level:
        suggestion = "\033[92mSuggested Buy\033[0m"  # Green text
    elif percentage_change < -0.5 and predicted_price_1h_ahead < support_level:
        suggestion = "\033[93mSuggested Sell\033[0m"  # Orange text
    elif 0.2 <= percentage_change <= 0.5:
        suggestion = "\033[92mShort Buy\033[0m"  # Orange text
    elif -0.5 <= percentage_change <= -0.2:
        suggestion = "\033[93mShort Sell\033[0m"  # Orange text
    elif -0.19 <= percentage_change <= 0.19:
        suggestion = "\033[90mNEUTRAL\033[0m"  # Grey text
    elif percentage_change >= 1.0:
        suggestion = "\033[92mSuggested Buy\033[0m"  # Green text
    elif percentage_change <= -1.0:
        suggestion = "\033[93mSuggested Sell\033[0m"  # Orange text
    else:
        suggestion = "No strong suggestion"

    # Print the requested outputs including the live price
    print(f"\nLive Ethereum Price: ${round(current_price, 2)}")
    print(f"Predicted Price in 1 Hour: ${round(predicted_price_1h_ahead, 2)}")
    print(f"Predicted Percentage Change: {round(percentage_change, 2)}%")
    print(f"Suggested Stop Loss: ${round(average_stop_loss, 2)}")
    print(f"Support Level: ${round(support_level, 2)}")
    print(f"Resistance Level: ${round(resistance_level, 2)}")
    print(suggestion)

def main():
    print("Type 'predict' to make a prediction and suggest a stop loss or 'exit' to quit.")

    while True:
        user_input = input("\nEnter command: ").strip().lower()
        
        if user_input == 'predict':
            make_prediction_and_suggest_stop_loss()
        elif user_input == 'exit':
            print("Exiting...")
            break
        elif user_input == 'price':
            show_live_price()
        else:
            print("Invalid command. Please type 'predict' or 'exit'.")

if __name__ == '__main__':
    main()

#Test 1: $2.01, Prediction: $2511.00, from $2507.89.
#Test 2: $, Prediction $2512.68 from $2509.88
