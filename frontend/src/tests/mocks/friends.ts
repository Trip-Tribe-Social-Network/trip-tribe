export const CURRENT_USER_FRIENDS = {
  user: {
    id: '2d3c4b18-91c6-4539-8a00-4d47f1bc65ac',
    name: 'Claire Dubois',
    email: 'claire.dubois@gmail.com',
    friends_count: 1,
    get_avatar: 'http://127.0.0.1:8000/media/avatars/AdobeStock_181193995_wzLNjCb.jpeg',
    friends: ['603961ae-28cd-4500-8315-6d89eb47080c']
  },
  friends: [
    {
      id: '603961ae-28cd-4500-8315-6d89eb47080c',
      name: 'Olivia Smith',
      email: 'olivia.smith@gmail.com',
      friends_count: 1,
      get_avatar: 'http://127.0.0.1:8000/media/avatars/AdobeStock_451071568_0lERyf2.jpeg',
      friends: ['2d3c4b18-91c6-4539-8a00-4d47f1bc65ac']
    }
  ],
  requests: [
    {
      id: 'b9a67438-f0a3-48bd-9155-882cd94bddc5',
      created_by: {
        id: '8e380c3b-d382-4709-ac86-f20db16b35da',
        name: 'Diego Fernandez',
        email: 'diego.fernandez@gmail.com',
        friends_count: 1,
        get_avatar:
          'http://127.0.0.1:8000/media/avatars/AdobeStock_479862394_LEGQsjY.jpeg',
        friends: []
      },
      status: 'sent',
      created_at: '2024-08-18T16:30:22.436434Z'
    }
  ]
}
