import asyncio

from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload # Дополнительная загрузка

from icecream import ic

from core.models import db_helper, User, Profile, Post


async def create_user(session: AsyncSession, username: str) -> User:
    user = User(username=username)
    session.add(user)
    await session.commit()
    ic(user)
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    # result: Result = await session.execute(stmt)
    # user: User | None = result.scalar_one_or_none()
    user: User | None = await session.scalar(stmt)
    ic(user)
    return user


async def create_user_profile(
    session: AsyncSession, user_id: int, first_name: str | None = None, last_name: str | None = None
) -> Profile:
    profile = Profile(user_id=user_id, first_name=first_name, last_name=last_name)
    session.add(profile)
    await session.commit()
    return profile


async def show_users_with_profiles(session: AsyncSession) -> list[User]:
    # Нужно сджоинить таблицы в асинхронном запросе
    stmt = select(User).options(joinedload(User.profile)).order_by(User.id)
    users = await session.scalars(stmt)
    for user in users:
        print(user)
        print(user.profile.first_name)


async def create_posts(session: AsyncSession, user_id: int, *post_titles: str) -> list[Post]:
    posts = [Post(title=title, user_id=user_id) for title in post_titles]
    session.add_all(posts)
    await session.commit()
    print(posts)
    return posts


async def get_users_with_posts(
        session: AsyncSession,
):
    # stmt = select(User).options(joinedload(User.posts)).order_by(User.id) # inner join
    stmt = (select(User).options(selectinload(User.posts))).order_by(User.id) # сначала юзеры, потом их посты
    result: Result = await session.execute(stmt)
    # users = result.scalars().unique()
    users = result.scalars()

    for user in users: # type: User 
        print("**" * 10)
        print(user)
        for post in user.posts:
            print("-", post)


async def get_posts_with_authors(session: AsyncSession):
    stmt = select(Post).options(joinedload(Post.user)).order_by(Post.id)
    posts = await session.scalars(stmt)

    for post in posts:
        print("post", post)
        print("author", post.user)


async def get_users_with_posts_and_profiles(session: AsyncSession):
    stmt = (
        select(User).options(selectinload(User.posts), joinedload(User.profile), ).order_by(User.id)
    )
    users = await session.scalars(stmt)

    # ic([user for user in users])
    for user in users: # type: User 
        print("**" * 10)
        print(user, user.profile and user.profile.first_name)
        for post in user.posts:
            print("-", post)


async def get_profiles_with_users_and_users_with_posts(session: AsyncSession):
    stmt = (
        select(Profile)
        .join(Profile.user) # для .where
        .options(
            joinedload(Profile.user).selectinload(User.posts),
        )
        .where(User.username == "john")
        .order_by(Profile.id)
    )

    profiles = await session.scalars(stmt)

    for profile in profiles:
        print(profile, profile.user)
        print(profile.user.posts)


async def main():
    async with db_helper.session_factory() as session:
        # await create_user(session=session, username="john")
        # await create_user(session=session, username="sam")
        # await create_user(session=session, username="alice")

        # user_john = await get_user_by_username(session=session, username="john")
        # user_sam = await get_user_by_username(session=session, username="sam")

        # ic(user_sam, user_john)
        
        # await create_user_profile(session, user_john.id, "john")
        # await create_user_profile(session, user_sam.id, "sam", "white")

        # await show_users_with_profiles(session=session)
        # await create_posts(session, user_john.id, "SQLA 2.0", "SQLA Joins")
        # await create_posts(session, user_sam.id, "FastAPI Advanced", "FastAPI more")

        # await get_users_with_posts(session=session)
        # await get_posts_with_authors(session=session)
        # await get_users_with_posts_and_profiles(session)
        await get_profiles_with_users_and_users_with_posts(session)


if __name__ == "__main__":
    asyncio.run(main())
