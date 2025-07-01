### Function Verification Checklist  
*(One test per scenario, each verifying one key behavior)*  

-  **Input Scenarios**  
   -  Valid inputs  
   -  Invalid inputs (errors/exceptions)  
   -  Edge cases (null, empty, min/max values)  

-  **Core Behavior**  
   - Return value  
   - Object state changes  
   - Output parameters (if applicable)  

-  **Side Effects**  
   -  Calls to dependencies (via mocks)  
   -  Changes to external resources  

-  **Resource Management**  
   -  No memory leaks (pointers/allocations)  
   -  Object lifecycle integrity  

-  **Error Handling**  
   - Exception types and messages  
   - Error codes  
   - State preservation on failure  

-  **Advanced (for complex operations)**  
   - Composite logic correctness  
   - Multi-step transaction integrity  
   - Concurrency safety (if applicable)  