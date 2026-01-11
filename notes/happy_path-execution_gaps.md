# Happy Path & Execution Gaps

## Happy Path

1. Order Received
2. Check Credit Score
3. Confirm Sale
4. Start Production
5. Finished Production
6. Load Shipment
7. Goods delivered

### Notes regarding Happy Path

- All processes include all these activities
- 43% have the proper start and ending ('Order received' and 'Goods delivered')
  - Average TPT: 65.4d (Median: 61d)
- Only 56 cases (0.28%) follow the _exact_ happy path
  - Average TPT: 47d

## Execution Gaps

### 1. Going back producing after loading shipment / finishing production

- WHEN: 'Finish production' and 'Load shipment' don't end in 'Deliver goods'
- 28% of all processes go to 'Change quantity' after 'Load shipment'
  - Adds 3h on average

### 2. Changing production start date

- WHEN: The activity "Change production start date" exists.
- 91% of all processes (!)
- 92% of all processes that start with 'Order received'
- Overall, the existence of this activity adds ~1d to the entire process (rough estimate with the Throughput Time Explorer)

### 3. Problems with the payment (& prices)

- WHEN: The activity "Credit order block" exists.
- 10% of all processes
- Processes don't immediately end after this
- 99% of all processes (even with the credit order block) have the "Check credit score", which may be related
- 82% of the 'Credit order block' processes also have a price change
- The credit order block is not a result of the check, but _ALWAYS_ a result of the "Order received"
- Average TPT between "Order received" and "Credit order block" is 3d
