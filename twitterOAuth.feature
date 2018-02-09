Feature: Twitter API oAuth test assignment


  Scenario: Check if user can be authenticated with right credentials
    Given we login with testUser and keys from environment variables TEST_USER_KEY and TEST_USER_SECRET
    Then user logged in successfully
    And user have been redirected to redirected url


  Scenario: Check if user can not be authenticated with wrong key
    Given we login with testUser and keys NOT_A_KEY and secret from environment variable TEST_USER_SECRET
    Then we get error from API


  Scenario: Check if user can not be authenticated with wrong secret
    Given we login with testUser and keys from environment variable TEST_USER_KEY and secret NOT_A_SECRET
    Then we get error from API


  Scenario: Check if user can not be authenticated with wrong user
    Given we login with notatestUser and keys from environment variables TEST_USER_KEY and TEST_USER_SECRET
    Then we get error from API


  Scenario: Check if user can not be authenticated with wrong user
    Given rate limit for testUser is bigger than zero
    Given we login with testUser and keys from environment variables TEST_USER_KEY and TEST_USER_SECRET
    Then user logged in successfully
    And user have been redirected to redirected url
    Then rate limit is lower by 1
    Given we login rate limit times
    Then rate limit is 1
    Given we login with testUser and keys from environment variables TEST_USER_KEY and TEST_USER_SECRET
    Then user logged in successfully
    Then rate limit is 0
    Given we login with testUser and keys from environment variables TEST_USER_KEY and TEST_USER_SECRET
    Then we get error from API which states that rate limit is reached


  Scenario: Check if system not fails for a very long username
    Given we login with very long username
    Then we get error from API


  Scenario: Check if system not fails for a very long key
    Given we login with testUser and keys from environment variables VERY_LONG_KEY and TEST_USER_SECRET
    Then we get error from API


  Scenario: Check if system not fails for a very long secret
    Given we login with testUser and keys from environment variables TEST_USER_KEY and VERY_LONG_KEY
    Then we get error from API


  Scenario: Check if system not fails for a illegal characters
    Given we login with test$%@User and keys from environment variables VERY_LONG_KEY and TEST_USER_SECRET
    Then we get error from API


  Scenario: Check if system not fails for a key with wrong characters
    Given we login with testUser and keys from environment variables KEY_WITH_ILLEGAL_CHARACTERS and TEST_USER_SECRET
    Then we get error from API


  Scenario: Check if system not fails for a secret with wrong characters
    Given we login with testUser and keys from environment variables TEST_USER_KEY and KEY_WITH_ILLEGAL_CHARACTERS
    Then we get error from API


   Scenario: Check if user can be authenticated with right credentials for a last time and our prvious examples did not broke the system
    Given we login with testUser and keys from environment variables TEST_USER_KEY and TEST_USER_SECRET
    Then user logged in successfully
    And user have been redirected to redirected url
