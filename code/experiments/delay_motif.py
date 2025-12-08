import numpy as np


def heaviside(x):
    return 1 if x >= 0 else 0


class DelayMotif:
    def __init__(self,
                 w1_V2=1.0, w1_U=0.0, alpha1=1.0, b1=-1.5, r=0.5,
                 w2=1.0, alpha2=1.0, b2=-1.5, s=0.5):
        """
        Initialize the 2-node delay motif.

        Node 1:
            V1_t = H(w1_V2 * V2_{t-1} + w1_U * U_t + alpha1 * eta1 + b1)
            eta1 ~ Bernoulli(r)

        Node 2:
            V2_t = H(w2 * V1_t + alpha2 * eta2 + b2)
            eta2 ~ Bernoulli(s)

        Y_t = V2_t
        """

        self.w1_V2 = w1_V2
        self.w1_U  = w1_U
        self.alpha1 = alpha1
        self.b1 = b1
        self.r = r  # noise probability for V1

        self.w2 = w2
        self.alpha2 = alpha2
        self.b2 = b2
        self.s = s  # noise probability for V2

        # internal memory state for V2
        self.V2 = 0  # initialize however you want
        
        # internal memory state for previous U
        self.U_prev = 0  # initialize to 0

    def step(self, U_t, eta1=None, eta2=None):
        """
        Simulate one time step given input U_t.
        
        Args:
            U_t: Input value
            eta1: Optional noise bit for V1 (if None, uses random)
            eta2: Optional noise bit for V2 (if None, uses random)
        
        Returns:
            (V1_t, V2_t, Y_t) tuple
        """

        # noise bits (use provided values or random)
        if eta1 is None:
            eta1 = np.random.rand() < self.r
        if eta2 is None:
            eta2 = np.random.rand() < self.s

        # compute V1_t
        # Use U_prev (which is U_{t-1}) instead of V2_{t-1} to track previous input
        # This allows V1 to directly depend on U_{t-1}
        V1_t = heaviside(
            self.w1_V2 * self.U_prev  # Use U_prev instead of V2 to track U_{t-1}
            + self.w1_U * U_t
            + self.alpha1 * eta1
            + self.b1
        )

        # compute V2_t
        V2_t = heaviside(
            self.w2 * V1_t
            + self.alpha2 * eta2
            + self.b2
        )

        # output
        Y_t = V2_t

        # update internal memory
        self.V2 = V2_t
        self.U_prev = U_t  # Store current U for next iteration

        return V1_t, V2_t, Y_t


# ---------------------------------------------------------
# Search function to find parameters meeting criteria
# ---------------------------------------------------------

def test_criteria(motif, test_inputs=[0, 1, 0, 1], verbose=False):
    """
    Test if the motif meets the criteria:
    - V2_t = U_{t-1} when eta1=eta2 (η(0,0) and η(1,1) have same V2 = U_{t-1})
    - V2_t ≠ U_{t-1} when eta1≠eta2 (η(0,1) and η(1,0) have same V2 ≠ U_{t-1})
    
    Returns: (meets_criteria, details_dict)
    """
    eta_combinations = [(0, 0), (0, 1), (1, 0), (1, 1)]
    all_match = True
    details = []
    
    # Reset motif state - start with V2 = 0, U_prev = 0
    motif.V2 = 0
    motif.U_prev = 0
    
    for u in test_inputs:
        saved_V2 = motif.V2
        saved_U_prev = motif.U_prev
        
        results = {}
        for eta1, eta2 in eta_combinations:
            motif.V2 = saved_V2
            motif.U_prev = saved_U_prev
            V1, V2, Y = motif.step(u, eta1=eta1, eta2=eta2)
            results[(eta1, eta2)] = V2
        
        # Check criteria
        # When eta1=eta2: V2 should equal U_{t-1}
        v2_00 = results[(0, 0)]
        v2_11 = results[(1, 1)]
        should_equal = saved_U_prev
        
        # When eta1≠eta2: V2 should be same but different from U_{t-1}
        v2_01 = results[(0, 1)]
        v2_10 = results[(1, 0)]
        should_differ = saved_U_prev
        
        # Check if criteria met
        match_00_11 = (v2_00 == should_equal) and (v2_11 == should_equal) and (v2_00 == v2_11)
        match_01_10 = (v2_01 == v2_10) and (v2_01 != should_differ)
        
        if not (match_00_11 and match_01_10):
            all_match = False
            if verbose:
                print(f"  Failed at U_prev={saved_U_prev}, U_t={u}: V2_00={v2_00}, V2_11={v2_11}, V2_01={v2_01}, V2_10={v2_10}")
        
        details.append({
            'U_prev': saved_U_prev,
            'U_t': u,
            'V2_00': v2_00,
            'V2_11': v2_11,
            'V2_01': v2_01,
            'V2_10': v2_10,
            'match_00_11': match_00_11,
            'match_01_10': match_01_10
        })
        
        # Update state for next iteration (use η(0,0) to update)
        motif.V2 = saved_V2
        motif.U_prev = saved_U_prev
        motif.step(u, eta1=0, eta2=0)
    
    return all_match, details


# ---------------------------------------------------------
# Example usage
# ---------------------------------------------------------

if __name__ == "__main__":
    # Search for parameters that meet the criteria
    print("Searching for parameters where:")
    print("  V2_t = U_{t-1} when η(0,0) and η(1,1)")
    print("  V2_t ≠ U_{t-1} when η(0,1) and η(1,0)")
    print()
    
    # Parameter ranges to search (expanded and focused)
    # Include negative weights which might help create flipping behavior
    w1_V2_range = [-1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0]
    w1_U_range = [-1.0, -0.5, 0.0, 0.5, 1.0]  # Allow negative U_t connection
    w2_range = [-1.0, -0.5, 0.5, 1.0, 1.5, 2.0]
    b1_range = [-2.0, -1.5, -1.0, -0.5, 0.0, 0.5]
    b2_range = [-2.5, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5]
    alpha1 = 1.0
    alpha2 = 1.0
    
    found = False
    test_inputs = [0, 1, 0, 1]
    
    for w1_V2 in w1_V2_range:
        for w1_U in w1_U_range:
            for w2 in w2_range:
                for b1 in b1_range:
                    for b2 in b2_range:
                        motif = DelayMotif(
                            w1_V2=w1_V2,
                            w1_U=w1_U,
                            alpha1=alpha1,
                            b1=b1,
                            r=1.0,
                            w2=w2,
                            alpha2=alpha2,
                            b2=b2,
                            s=1.0
                        )
                        
                        meets, details = test_criteria(motif, test_inputs)
                        
                        if meets:
                            print(f"Found matching parameters!")
                            print(f"  w1_V2={w1_V2}, w1_U={w1_U}, w2={w2}, b1={b1}, b2={b2}")
                            print(f"  alpha1={alpha1}, alpha2={alpha2}")
                            print()
                            
                            # Use these parameters for the full display
                            motif = DelayMotif(
                                w1_V2=w1_V2, w1_U=w1_U, alpha1=alpha1, b1=b1, r=1.0,
                                w2=w2, alpha2=alpha2, b2=b2, s=1.0
                            )
                            found = True
                            break
                    
                    if found:
                        break
                if found:
                    break
            if found:
                break
        if found:
            break
    
    if not found:
        print("No matching parameters found in search space.")
        print("Trying a few targeted combinations...")
        
        # Try some promising combinations based on dynamics analysis
        # We need: when eta1=eta2, V2 = U_{t-1}; when eta1≠eta2, V2 ≠ U_{t-1}
        # Key insight: When both eta=1, we get +1 to both, which always pushes to 1.
        # We need the noise to work with the signal, not just override it.
        # Try: Use negative alpha or adjust weights so noise cancels appropriately
        test_configs = [
            # Try negative weights which might help create flipping behavior
            # Systematic exploration of negative weight combinations
            # Negative w1_V2 (inverts U_prev signal)
            (-1.0, 0.0, 1.0, -0.5, -0.5),
            (-1.0, 0.0, 1.0, 0.0, -0.5),
            (-1.0, 0.0, 1.0, -0.5, 0.0),
            (-1.5, 0.0, 1.0, -0.5, -0.5),
            (-1.0, 0.0, 1.5, -0.5, -0.5),
            # Negative w2 (inverts V1)
            (1.0, 0.0, -1.0, -0.5, -0.5),
            (1.0, 0.0, -1.0, 0.0, -0.5),
            (1.0, 0.0, -1.0, -0.5, 0.0),
            (1.5, 0.0, -1.0, -0.5, -0.5),
            (1.0, 0.0, -1.5, -0.5, -0.5),
            # Both negative (double inversion = same as positive, but different dynamics)
            (-1.0, 0.0, -1.0, -0.5, -0.5),
            (-1.0, 0.0, -1.0, 0.0, -0.5),
            (-1.0, 0.0, -1.0, -0.5, 0.0),
            (-1.5, 0.0, -1.0, -0.5, -0.5),
            (-1.0, 0.0, -1.5, -0.5, -0.5),
            # Negative w1_U
            (1.0, -0.5, 1.0, -0.5, -0.5),
            (1.0, -1.0, 1.0, -0.5, -0.5),
            # Combinations with adjusted biases
            (-1.0, 0.0, 1.0, -1.0, -1.0),
            (1.0, 0.0, -1.0, -1.0, -1.0),
            (-1.0, 0.0, -1.0, -1.0, -1.0),
            (-1.0, 0.0, 1.0, -1.0, -0.5),
            (1.0, 0.0, -1.0, -1.0, -0.5),
        ]
        
        # Also try with different alpha values to reduce noise impact
        alpha_configs = [
            (1.0, 0.0, 1.0, -1.0, -1.0, 0.5, 0.5),  # Reduced noise
            (1.0, 0.0, 1.0, -1.5, -1.5, 0.5, 0.5),
        ]
        
        for w1_V2, w1_U, w2, b1, b2 in test_configs:
            motif_test = DelayMotif(
                w1_V2=w1_V2, w1_U=w1_U, alpha1=1.0, b1=b1, r=1.0,
                w2=w2, alpha2=1.0, b2=b2, s=1.0
            )
            meets, details = test_criteria(motif_test, test_inputs, verbose=False)
            if meets:
                print(f"Found! Config: w1_V2={w1_V2}, w1_U={w1_U}, w2={w2}, b1={b1}, b2={b2}")
                motif = motif_test
                found = True
                break
            else:
                # Show why it failed for first config
                if w1_V2 == test_configs[0][0]:
                    print(f"Testing config (w1_V2={w1_V2}, w1_U={w1_U}, w2={w2}, b1={b1}, b2={b2}):")
                    test_criteria(motif_test, test_inputs, verbose=True)
        
        if not found:
            print("Using default parameters for display...")
            motif = DelayMotif(
                w1_V2=2.0, w1_U=0.0, alpha1=1.0, b1=-0.5, r=1.0,
                w2=2.0, alpha2=1.0, b2=-0.5, s=1.0
            )

    # simulate with some input sequence
    inputs = [0,1,1,0,1,0,0,1,1,0]
    
    # All 4 combinations of eta1 and eta2
    eta_combinations = [(0, 0), (0, 1), (1, 0), (1, 1)]
    
    # Print header with columns for each eta combination
    # Data format: "     (0,0)     |" = 16 chars total (15 content + 1 |)
    data_col_format = "     ({},{})     |"
    col_width = len(data_col_format.format(0, 0))  # Should be 16
    
    # First column data format: " 0   |" = 6 chars total
    first_col_data = " 0   |"
    first_col_width = len(first_col_data)  # Should be 6
    header = "U_{t-1} | U_t  |"  # Add extra space to match data width
    for eta1, eta2 in eta_combinations:
        header_text = f"η({eta1},{eta2}) V1,V2"
        # Center the header text in the column (col_width - 1 for the |)
        total_width = col_width - 1  # 15 chars for content
        padding_left = (total_width - len(header_text)) // 2
        padding_right = total_width - len(header_text) - padding_left
        header += " " * padding_left + header_text + " " * padding_right + "|"
    print(header)
    print("-" * len(header))
    
    # Loop through each input
    for u in inputs:
        # Save current V2 and U_prev state before testing all combinations
        saved_V2 = motif.V2
        saved_U_prev = motif.U_prev
        
        # Collect results for all eta combinations
        results = []
        for eta1, eta2 in eta_combinations:
            # Reset V2 and U_prev to saved state for each combination
            motif.V2 = saved_V2
            motif.U_prev = saved_U_prev
            
            V1, V2, Y = motif.step(u, eta1=eta1, eta2=eta2)
            results.append((V1, V2))
        
        # Print row with previous U, current U, and all results
        row = f"  {saved_U_prev}    |  {u}   |"
        for V1, V2 in results:
            row += f"     ({V1},{V2})     |"
        print(row)
        
        # Update V2 and U_prev for next input (use first combination's result)
        motif.V2 = saved_V2
        motif.U_prev = saved_U_prev
        motif.step(u, eta1=0, eta2=0)  # Update state using first combination

