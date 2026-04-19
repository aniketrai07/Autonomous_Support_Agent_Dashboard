# Failure Modes & Handling

## 1. Missing Order ID

* Agent asks user for order ID
* Stops further processing

## 2. Order Not Found

* Agent informs user
* Prevents incorrect refund

## 3. Tool Failure (Timeout)

* Retry mechanism applied
* Ensures robustness

## 4. Low Confidence Case

* Agent escalates to human support

## 5. Ambiguous Request

* Agent sends clarification response

## 6. Invalid Input

* Safe fallback message used
